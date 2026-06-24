from fpdf import FPDF
from database.db import query_db
from controllers.students_controller import get_all_students
from controllers.teams_controller import get_all_teams


# --- Helpers de PDF ---

def sanitize_text(value):
    if value is None:
        text = ""
    else:
        text = str(value)

    return text.encode("latin-1", "replace").decode("latin-1")


def new_pdf():
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    return pdf


def pdf_bytes(pdf):
    return bytes(pdf.output())


def section_title(pdf, titulo, subtitulo=None):
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, sanitize_text(titulo), new_x="LMARGIN", new_y="NEXT", align="C")

    if subtitulo:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 7, sanitize_text(subtitulo), new_x="LMARGIN", new_y="NEXT", align="C")

    pdf.ln(3)


def table(pdf, headers, widths, rows):
    pdf.set_font("Helvetica", "B", 11)
    for header, width in zip(headers, widths):
        pdf.cell(width, 8, sanitize_text(header), border=1, align="C")
    pdf.ln()

    pdf.set_font("Helvetica", "", 10)
    if not rows:
        pdf.cell(sum(widths), 8, sanitize_text("Sin registros"), border=1, align="C")
        pdf.ln()
        return

    for row in rows:
        for value, width in zip(row, widths):
            pdf.cell(width, 7, sanitize_text(value), border=1)
        pdf.ln()


# --- Helpers de datos ---
def query_marks(id_curso, evaluaciones):
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

    evaluaciones_filtradas = []

    for ev in evaluaciones:
        if ev:
            evaluaciones_filtradas.append(ev)
    evaluaciones = evaluaciones_filtradas

    if evaluaciones:
        placeholders = ", ".join(["%s"] * len(evaluaciones))
        sql += f" AND t.nombre IN ({placeholders})"
        params.extend(evaluaciones)

    sql += " ORDER BY a.apellido, a.nombre, t.nombre"
    return query_db(sql, params), evaluaciones


def calc_estados(id_curso):
    cfg = query_db(
        "SELECT es_promocionable FROM curso_promocion_config WHERE id_curso = %s",
        (int(id_curso),)
    )

    if cfg:
        es_promocionable = bool(cfg[0]["es_promocionable"])
    else:
        es_promocionable = False

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

    estado_por_alumno = {}
    for row in promedios:
        if row["promedio"] is not None:
            prom = float(row["promedio"])
        else:
            prom = 0

        if es_promocionable:
            if prom >= 7:
                estado = "Promociona"
            elif prom >= 4:
                estado = "Final"
            else:
                estado = "Recursa"
        else:
            if prom >= 4:
                estado = "Aprobado"
            else:
                estado = "Desaprobado"

        estado_por_alumno[row["id_alumno"]] = estado

    return estado_por_alumno


# --- Section builders ---

def add_students_section(pdf, id_curso, subtitulo=None):
    result = get_all_students({"id_curso": id_curso})

    if not result["ok"]:
        return result

    section_title(pdf, "Listado de Alumnos", subtitulo)

    rows = []
    
    for a in result["data"]:
        if a.get("estado_alumno"):
            estado = "Activo"
        else:
            estado = "Baja"

        rows.append((
            a["padron"],
            a["apellido"],
            a["nombre"],
            a["correo"],
            estado,
        ))

    table(pdf, ["Padrón", "Apellido", "Nombre", "Correo", "Estado"], [25, 40, 40, 60, 25], rows)
    return None


def add_teams_section(pdf, id_curso, subtitulo=None):
    result = get_all_teams({"id_curso": id_curso})

    if not result["ok"]:
        return result

    section_title(pdf, "Reporte de Equipos", subtitulo)
    equipos = result["data"]

    if not equipos:
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, sanitize_text("No hay equipos registrados"), new_x="LMARGIN", new_y="NEXT")
        return None

    for equipo in equipos:
        pdf.set_font("Helvetica", "B", 12)
        pdf.ln(2)
        pdf.cell(0, 8, sanitize_text(equipo["nombre_equipo"]), new_x="LMARGIN", new_y="NEXT")

        rows = []
        for al in equipo.get("alumnos", []):
            rows.append((al["padron"], al["apellido"], al["nombre"]))

        table(pdf, ["Padrón", "Apellido", "Nombre"], [30, 60, 60], rows)

    return None


def add_marks_section(pdf, id_curso, evaluaciones=None, mostrar_corrector=False, incluir_estado_final=False, subtitulo=None):
    notas, evaluaciones  = query_marks(id_curso, evaluaciones)
    estado_por_alumno    = calc_estados(id_curso) if incluir_estado_final else {}

    section_title(pdf, "Reporte de Notas", subtitulo)

    PAGE_W     = 190
    W_PADRON   = 22
    W_NOTA     = 15
    W_CORRECTOR = 30
    W_ESTADO   = 22

    fixed = W_PADRON + W_NOTA
    if mostrar_corrector:
        fixed += W_CORRECTOR
    if incluir_estado_final:
        fixed += W_ESTADO

    flexible = PAGE_W - fixed
    W_ALUMNO = round(flexible * 0.55)
    W_EVAL   = flexible - W_ALUMNO

    headers = ["Padrón", "Alumno", "Evaluación", "Nota"]
    widths  = [W_PADRON, W_ALUMNO, W_EVAL, W_NOTA]

    if mostrar_corrector:
        headers.append("Corrector")
        widths.append(W_CORRECTOR)
    if incluir_estado_final:
        headers.append("Estado")
        widths.append(W_ESTADO)

    rows = []
    for n in notas:
        row = [
            n["padron"],
            f"{n['apellido']}, {n['nombre']}",
            n["evaluacion"],
            n["nota"],
        ]
        if mostrar_corrector:
            row.append(n.get("corrector_nombre") or "—")
        if incluir_estado_final:
            row.append(estado_por_alumno.get(n.get("id_alumno"), "—"))

        rows.append(row)

    table(pdf, headers, widths, rows)
    return None


def add_attendance_section(pdf, id_curso, subtitulo=None):
    alumnos = query_db(
        "SELECT id_alumno, padron, apellido, nombre FROM alumnos WHERE id_curso = %s AND estado_alumno = 1 ORDER BY apellido, nombre",
        (int(id_curso),)
    )
    if not alumnos:
        return None

    ids = []
    for a in alumnos:
        ids.append(a["id_alumno"])

    clases       = query_db("SELECT COUNT(*) AS total FROM clases WHERE id_curso = %s", (int(id_curso),))
    total_clases = clases[0]["total"] if clases else 0

    fmt       = ",".join(["%s"] * len(ids))
    presencias = query_db(
        f"SELECT id_alumno, COUNT(*) AS presentes FROM asistencia WHERE id_alumno IN ({fmt}) AND presente != 0 GROUP BY id_alumno",
        ids
    )

    presencias_map = {}
    for r in presencias:
        presencias_map[r["id_alumno"]] = r["presentes"]

    section_title(pdf, "Asistencia por Alumno", subtitulo)

    rows = []
    for a in alumnos:
        presentes = presencias_map.get(a["id_alumno"], 0)
        pct       = round(presentes / total_clases * 100, 1) if total_clases else 0

        rows.append((
            a["padron"],
            f"{a['apellido']}, {a['nombre']}",
            f"{presentes}/{total_clases}",
            f"{pct}%",
        ))

    table(pdf, ["Padrón", "Alumno", "Presencias", "%"], [25, 80, 30, 20], rows)
    return None


# --- Función principal ---

def report_combined_pdf(opciones):
    id_curso = opciones.get("id_curso")

    if not id_curso:
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "Falta el parámetro curso_id"}

    incluir_alumnos    = opciones.get("incluir_alumnos")
    incluir_equipos    = opciones.get("incluir_equipos")
    incluir_notas      = opciones.get("incluir_notas")
    incluir_asistencia = opciones.get("incluir_asistencia")

    if not any([incluir_alumnos, incluir_equipos, incluir_notas, incluir_asistencia]):
        return {"ok": False, "code": 400, "message": "Bad Request",
                "description": "Seleccioná al menos una sección para exportar"}

    try:
        materia              = opciones.get("materia")
        catedra              = opciones.get("catedra")
        cuatrimestre         = opciones.get("cuatrimestre")
        anio                 = opciones.get("anio")
        evaluaciones         = opciones.get("evaluaciones")
        mostrar_corrector    = opciones.get("mostrar_corrector")
        incluir_estado_final = opciones.get("incluir_estado_final")

        if cuatrimestre or anio:
            periodo = f"{cuatrimestre} {anio}".strip()
        else:
            periodo = None

        partes = []
        for p in [materia, catedra, periodo]:
            if p:
                partes.append(p)

        if partes:
            subtitulo = " · ".join(partes)
        else:
            subtitulo = None

        pdf = new_pdf()

        if incluir_alumnos:
            err = add_students_section(pdf, id_curso, subtitulo)
            if err:
                return err
        if incluir_notas:
            err = add_marks_section(pdf, id_curso, evaluaciones, mostrar_corrector, incluir_estado_final, subtitulo)
            if err:
                return err
        if incluir_asistencia:
            err = add_attendance_section(pdf, id_curso, subtitulo)
            if err:
                return err
        if incluir_equipos:
            err = add_teams_section(pdf, id_curso, subtitulo)
            if err:
                return err

        return {
            "ok":       True,
            "data":     pdf_bytes(pdf),
            "filename": f"informe_curso_{id_curso}.pdf",
        }

    except Exception as e:
        return {"ok": False, "code": 500, "message": "Internal Server Error",
                "description": str(e)}
