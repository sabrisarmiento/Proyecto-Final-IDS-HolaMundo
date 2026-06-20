from database.db import query_db


def get_course_dashboard(id_curso):
    try:
        # alumnos
        alumnos_raw = query_db(
            """
            SELECT id_alumno, nombre, apellido, estado_alumno
            FROM alumnos
            WHERE id_curso = %s
            """,
            (id_curso,)
        )

        total_alumnos = len(alumnos_raw)
        activos       = [a for a in alumnos_raw if a["estado_alumno"]]
        abandonaron   = total_alumnos - len(activos)
        ids_activos   = [a["id_alumno"] for a in activos]

        # equipos
        equipos_count = query_db(
            "SELECT COUNT(*) AS total FROM equipos WHERE id_curso = %s",
            (id_curso,)
        )[0]["total"]

        # evaluaciones del curso
        evaluaciones = query_db(
            """
            SELECT e.id_evaluacion, t.nombre
            FROM evaluaciones e
            JOIN tipos_evaluacion t ON e.id_tipo = t.id_tipo
            WHERE e.id_curso = %s
            ORDER BY e.id_evaluacion ASC
            """,
            (id_curso,)
        )

        # notas de alumnos activos
        notas_por_alumno = {}
        promedio_por_eval = {}

        if ids_activos and evaluaciones:
            fmt = ",".join(["%s"] * len(ids_activos))
            notas_raw = query_db(
                f"""
                SELECT id_alumno, id_evaluacion, nota
                FROM notas
                WHERE id_alumno IN ({fmt})
                """,
                ids_activos
            )

            eval_notas = {}
            for n in notas_raw:
                notas_por_alumno.setdefault(n["id_alumno"], []).append(float(n["nota"]))
                eval_notas.setdefault(n["id_evaluacion"], []).append(float(n["nota"]))

            for ev in evaluaciones:
                vals = eval_notas.get(ev["id_evaluacion"], [])
                promedio_por_eval[ev["id_evaluacion"]] = (
                    round(sum(vals) / len(vals), 2) if vals else None
                )

        todos_valores = [v for vs in notas_por_alumno.values() for v in vs]
        promedio_general = (
            round(sum(todos_valores) / len(todos_valores), 2) if todos_valores else None
        )

        promo_cfg_raw = query_db(
            "SELECT es_promocionable, cuenta_asistencia, porcentaje_asistencia FROM curso_promocion_config WHERE id_curso = %s",
            (id_curso,)
        )
        if promo_cfg_raw:
            es_promocionable      = bool(promo_cfg_raw[0]["es_promocionable"])
            cuenta_asistencia     = bool(promo_cfg_raw[0]["cuenta_asistencia"])
            porcentaje_asistencia = float(promo_cfg_raw[0]["porcentaje_asistencia"])
        else:
            es_promocionable      = False
            cuenta_asistencia     = False
            porcentaje_asistencia = 75.0

        umbral_asistencia = porcentaje_asistencia if (es_promocionable and cuenta_asistencia) else 75.0

        promo_evals = {}
        if es_promocionable:
            pe = query_db(
                """
                SELECT id_evaluacion, cuenta_para_promocion, nota_minima
                FROM configuracion_promocion
                WHERE id_curso = %s AND cuenta_para_promocion = 1
                """,
                (id_curso,)
            )
            for row in pe:
                promo_evals[row["id_evaluacion"]] = float(row["nota_minima"]) if row["nota_minima"] is not None else 4.0

        notas_por_alumno_eval = {}
        if ids_activos and evaluaciones:
            fmt = ",".join(["%s"] * len(ids_activos))
            notas_full = query_db(
                f"""
                SELECT id_alumno, id_evaluacion, nota
                FROM notas
                WHERE id_alumno IN ({fmt})
                """,
                ids_activos
            )
            for n in notas_full:
                notas_por_alumno_eval.setdefault(n["id_alumno"], {})[n["id_evaluacion"]] = float(n["nota"])

        clases = query_db(
            "SELECT id_clase, fecha, temas FROM clases WHERE id_curso = %s ORDER BY fecha ASC, id_clase ASC",
            (id_curso,)
        )
        total_clases = len(clases)

        pct_asistencia_por_alumno = {}
        asistencia_stats = {"regulares": 0, "en_riesgo": 0, "sin_datos": 0}
        attendance_by_student = []
        presentes_pares = []

        if total_clases > 0 and ids_activos:
            fmt = ",".join(["%s"] * len(ids_activos))
            presencias = query_db(
                f"""
                SELECT id_alumno, COUNT(*) AS presentes
                FROM asistencia
                WHERE id_alumno IN ({fmt}) AND presente != 0
                GROUP BY id_alumno
                """,
                ids_activos
            )
            presencias_map = {r["id_alumno"]: r["presentes"] for r in presencias}
            names_map = {a["id_alumno"]: a for a in activos}

            presentes_raw = query_db(
                f"""
                SELECT id_alumno, id_clase
                FROM asistencia
                WHERE id_alumno IN ({fmt}) AND presente != 0
                """,
                ids_activos
            )
            presentes_pares = [[r["id_alumno"], r["id_clase"]] for r in presentes_raw]

            for aid in ids_activos:
                presentes = presencias_map.get(aid, 0)
                pct = (presentes / total_clases) * 100
                pct_asistencia_por_alumno[aid] = pct

                if pct >= umbral_asistencia:
                    asistencia_stats["regulares"] += 1
                else:
                    asistencia_stats["en_riesgo"] += 1

                alumno = names_map.get(aid, {})
                attendance_by_student.append({
                    "id_alumno":    aid,
                    "nombre":       alumno.get("nombre"),
                    "apellido":     alumno.get("apellido"),
                    "presentes":    presentes,
                    "total_clases": total_clases,
                    "porcentaje":   round(pct, 1),
                })
        else:
            asistencia_stats["sin_datos"] = len(ids_activos)
            for aid in ids_activos:
                pct_asistencia_por_alumno[aid] = None

        promocionados = 0
        van_a_final   = 0
        recursantes   = 0

        for alumno_id in ids_activos:
            notas_alumno = notas_por_alumno_eval.get(alumno_id, {})
            valores = list(notas_alumno.values())

            if not valores:
                van_a_final += 1
                continue

            recursa = any(v < 4 for v in valores)
            if recursa:
                recursantes += 1
                continue

            if es_promocionable:
                if promo_evals:
                    cumple_notas = all(
                        notas_alumno.get(id_ev, 0) >= nota_min
                        for id_ev, nota_min in promo_evals.items()
                    )
                else:
                    cumple_notas = True

                if cuenta_asistencia and total_clases > 0:
                    pct_asist = pct_asistencia_por_alumno.get(alumno_id)
                    cumple_asistencia = (pct_asist is not None and pct_asist >= porcentaje_asistencia)
                else:
                    cumple_asistencia = True

                if cumple_notas and cumple_asistencia:
                    promocionados += 1
                else:
                    van_a_final += 1
            else:
                promedio_alumno = sum(valores) / len(valores)
                if promedio_alumno >= 4:
                    van_a_final += 1
                else:
                    recursantes += 1

        presentes_totales = len(presentes_pares)
        posibles_totales = total_clases * len(ids_activos)
        asistencia_general_pct = round(presentes_totales / posibles_totales * 100, 1) if posibles_totales else 0

        return {
            "ok": True,
            "data": {
                "alumnos": {
                    "total":      total_alumnos,
                    "activos":    len(ids_activos),
                    "abandonaron": abandonaron,
                },
                "equipos": equipos_count,
                "clasificacion": {
                    "promocionados": promocionados,
                    "van_a_final":   van_a_final,
                    "recursantes":   recursantes,
                    "abandonaron":   abandonaron,
                },
                "promedio_general": promedio_general,
                "evaluaciones": [
                    {
                        "id":      ev["id_evaluacion"],
                        "nombre":  ev["nombre"],
                        "promedio": promedio_por_eval.get(ev["id_evaluacion"]),
                    }
                    for ev in evaluaciones
                ],
                "asistencia": {
                    **asistencia_stats,
                    "umbral": umbral_asistencia,
                },
                "asistencia_detalle": attendance_by_student,
                "asistencia_general": {
                    "porcentaje": asistencia_general_pct,
                    "presentes":  presentes_totales,
                    "posibles":   posibles_totales,
                },
                "clases_list": [
                    {"id_clase": c["id_clase"], "fecha": c["fecha"], "temas": c["temas"]}
                    for c in clases
                ],
                "alumnos_list": [
                    {"id_alumno": a["id_alumno"], "nombre": a["nombre"], "apellido": a["apellido"]}
                    for a in activos
                ],
                "presentes": presentes_pares,
                "es_promocionable":   es_promocionable,
            }
        }

    except Exception as e:
        return {
            "ok": False,
            "code": 500,
            "message": "Internal Server Error",
            "description": str(e)
        }