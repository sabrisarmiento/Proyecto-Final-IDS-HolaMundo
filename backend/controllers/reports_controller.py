from fpdf import FPDF
from database.db import query_db
from controllers.students_controller import get_all_students
from controllers.teams_controller import get_all_teams


def _s(value):
    """Sanea texto para las fuentes core de fpdf (latin-1)."""
    return str(value if value is not None else "").encode("latin-1", "replace").decode("latin-1")


def _new_pdf():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    return pdf


def _section_title(pdf, titulo, subtitulo=None):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, _s(titulo), new_x="LMARGIN", new_y="NEXT", align="C")
    if subtitulo:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, _s(subtitulo), new_x="LMARGIN", new_y="NEXT", align="C")
    pdf.ln(3)


def _table(pdf, headers, widths, rows):
    pdf.set_font("Helvetica", "B", 11)
    for header, width in zip(headers, widths):
        pdf.cell(width, 8, _s(header), border=1, align="C")
    pdf.ln()
    pdf.set_font("Helvetica", "", 10)
    if not rows:
        pdf.cell(sum(widths), 8, _s("Sin registros"), border=1, align="C")
        pdf.ln()
        return
    for row in rows:
        for value, width in zip(row, widths):
            pdf.cell(width, 7, _s(value), border=1)
        pdf.ln()


def _pdf_bytes(pdf):
    return bytes(pdf.output())


# --- Section builders: agregan una sección al pdf, devuelven dict de error o None ---

def _add_students_section(pdf, id_curso):
    result = get_all_students({"id_curso": id_curso})
    if not result["ok"]:
        return result
    _section_title(pdf, "Listado de Alumnos", f"Curso ID {id_curso}")
    rows = [
        (a["padron"], a["apellido"], a["nombre"], a["correo"],
         "Activo" if a.get("estado_alumno") else "Baja")
        for a in result["data"]
    ]
    _table(pdf, ["Padrón", "Apellido", "Nombre", "Correo", "Estado"],
           [25, 40, 40, 60, 25], rows)
    return None


def _add_teams_section(pdf, id_curso):
    result = get_all_teams({"id_curso": id_curso})
    if not result["ok"]:
        return result
    _section_title(pdf, "Reporte de Equipos", f"Curso ID {id_curso}")
    equipos = result["data"]
    if not equipos:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, _s("No hay equipos registrados"),
                 new_x="LMARGIN", new_y="NEXT")
        return None
    for equipo in equipos:
        pdf.set_font("Helvetica", "B", 12)
        pdf.ln(2)
        pdf.cell(0, 8, _s(equipo["nombre_equipo"]), new_x="LMARGIN", new_y="NEXT")
        rows = [(al["padron"], al["apellido"], al["nombre"])
                for al in equipo.get("alumnos", [])]
        _table(pdf, ["Padrón", "Apellido", "Nombre"], [30, 60, 60], rows)
    return None


def _add_marks_section(pdf, id_curso, evaluaciones=None, mostrar_corrector=False, incluir_estado_final=False):
    sql = """
        SELECT a.id_alumno, a.padron, a.apellido, a.nombre, t.nombre AS evaluacion, n.nota,
               n.corrector_nombre
        FROM notas n
        JOIN evaluaciones e ON n.id_evaluacion = e.id_evaluacion
        JOIN tipos_evaluacion t ON e.id_tipo = t.id_tipo
        JOIN alumnos a ON n.id_alumno = a.id_alumno
        WHERE e.id_curso = %s
    """
    params = [int(id_curso)]

    evaluaciones = [ev for ev in (evaluaciones or []) if ev]
    if evaluaciones:
        placeholders = ", ".join(["%s"] * len(evaluaciones))
        sql += f" AND t.nombre IN ({placeholders})"
        params.extend(evaluaciones)

    sql += " ORDER BY a.apellido, a.nombre, t.nombre"
    notas = query_db(sql, params)

    estado_por_alumno = {}
    if incluir_estado_final:
        cfg = query_db(
            "SELECT es_promocionable FROM curso_promocion_config WHERE id_curso = %s",
            (int(id_curso),)
        )
        es_promocionable = bool(cfg[0]["es_promocionable"]) if cfg else False

        promedios = query_db(
            """
            SELECT a.id_alumno, AVG(n.nota) AS promedio
            FROM notas n
            JOIN evaluaciones e ON n.id_evaluacion = e.id_evaluacion
            JOIN alumnos a ON n.id_alumno = a.id_alumno
            WHERE e.id_curso = %s
            GROUP BY a.id_alumno
            """,
            (int(id_curso),)
        )
        for row in promedios:
            prom = float(row["promedio"]) if row["promedio"] is not None else 0
            if es_promocionable:
                if prom >= 7:
                    estado = "Promociona"
                elif prom >= 4:
                    estado = "Final"
                else:
                    estado = "Recursa"
            else:
                estado = "Aprobado" if prom >= 4 else "Desaprobado"
            estado_por_alumno[row["id_alumno"]] = estado

    filtro = ", ".join(evaluaciones) if evaluaciones else "todas las evaluaciones"
    _section_title(pdf, "Reporte de Notas", f"Curso ID {id_curso} - {filtro}")

    headers = ["Padrón", "Alumno", "Evaluación", "Nota"]
    widths  = [25, 65, 45, 20]
    if mostrar_corrector:
        headers.append("Corrector")
        widths.append(35)
    if incluir_estado_final:
        headers.append("Estado")
        widths.append(25)

    rows = []
    for n in notas:
        row = [n["padron"], f"{n['apellido']}, {n['nombre']}", n["evaluacion"], n["nota"]]
        if mostrar_corrector:
            row.append(n.get("corrector_nombre") or "—")
        if incluir_estado_final:
            row.append(estado_por_alumno.get(n.get("id_alumno"), "—"))
        rows.append(row)

    _table(pdf, headers, widths, rows)
    return None


def _add_attendance_section(pdf, id_curso):
    alumnos = query_db(
        "SELECT id_alumno, padron, apellido, nombre FROM alumnos WHERE id_curso = %s AND estado_alumno = 1 ORDER BY apellido, nombre",
        (int(id_curso),)
    )
    if not alumnos:
        return None

    ids = [a["id_alumno"] for a in alumnos]
    clases = query_db(
        "SELECT COUNT(*) AS total FROM clases WHERE id_curso = %s",
        (int(id_curso),)
    )
    total_clases = clases[0]["total"] if clases else 0

    fmt = ",".join(["%s"] * len(ids))
    presencias = query_db(
        f"SELECT id_alumno, COUNT(*) AS presentes FROM asistencia WHERE id_alumno IN ({fmt}) AND presente != 0 GROUP BY id_alumno",
        ids
    )
    presencias_map = {r["id_alumno"]: r["presentes"] for r in presencias}

    _section_title(pdf, "Asistencia por Alumno", f"Curso ID {id_curso}")
    rows = []
    for a in alumnos:
        presentes = presencias_map.get(a["id_alumno"], 0)
        pct = round(presentes / total_clases * 100, 1) if total_clases else 0
        rows.append((a["padron"], f"{a['apellido']}, {a['nombre']}",
                     f"{presentes}/{total_clases}", f"{pct}%"))
    _table(pdf, ["Padrón", "Alumno", "Presencias", "%"], [25, 80, 30, 20], rows)
    return None


# --- Endpoint combinado: un solo PDF según lo seleccionado ---

def report_combined_pdf(id_curso, incluir_alumnos, incluir_equipos,
                        incluir_notas, evaluaciones=None,
                        incluir_asistencia=False, mostrar_corrector=False,
                        incluir_estado_final=False):
    if not id_curso:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "Falta el parámetro curso_id"}
    if not any([incluir_alumnos, incluir_equipos, incluir_notas, incluir_asistencia]):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "Seleccioná al menos una sección para exportar"}
    try:
        pdf = _new_pdf()
        if incluir_alumnos:
            err = _add_students_section(pdf, id_curso)
            if err:
                return err
        if incluir_notas:
            err = _add_marks_section(pdf, id_curso, evaluaciones, mostrar_corrector, incluir_estado_final)
            if err:
                return err
        if incluir_asistencia:
            err = _add_attendance_section(pdf, id_curso)
            if err:
                return err
        if incluir_equipos:
            err = _add_teams_section(pdf, id_curso)
            if err:
                return err
        return {"ok": True, "data": _pdf_bytes(pdf),
                "filename": f"informe_curso_{id_curso}.pdf"}
    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}
