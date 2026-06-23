from config import BASE_URL
from flask import render_template, request, redirect, url_for, session
import requests

from . import courses_bp
from .common import BACKEND_URL, get_token
from services.advertisements_service import get_advertisements_by_course, get_all_combined_advertisements, get_slack_advertisements_by_course
from services.courses_service import get_course_by_id
from services.students_services import post_student
from services.exams_service import get_exams_by_course_id
from services.material_frontend_service import get_materials_by_course


@courses_bp.route('/cursos/<int:course_id>', methods=['GET', 'POST'])
def course_detail(course_id):
    token = session.get("token")
    user = session.get("user", {})

    if not token or not user:
        return redirect(url_for("landing.landing") + "?error=Debes iniciar sesión")
    
    id_user = user.get("id_usuario")
    nivel = user.get("nivel")
    id_rol = user.get("id_rol")


    try:
        assistants_res = requests.get(
            f'{BACKEND_URL}/courses/{course_id}/assistants',
            headers=headers
        )

        assistants_data = assistants_res.json() if assistants_res.ok else {}
        assistants = assistants_data.get("assistants") or assistants_data.get("data") or []

    except Exception as e:
        print(f"Error cargando ayudantes del curso: {e}")
        assistants = []


    try:
        available_assistants_res = requests.get(
            f'{BACKEND_URL}/users',
            params={"id_rol": 3},
            headers=headers
        )

        available_assistants_data = available_assistants_res.json() if available_assistants_res.ok else {}
        available_assistants = available_assistants_data.get("users") or available_assistants_data.get("data") or []
        print("STATUS AVAILABLE ASSISTANTS:", available_assistants_res.status_code)
        print("JSON AVAILABLE ASSISTANTS:", available_assistants_data)
        print("AVAILABLE ASSISTANTS:", available_assistants)

    except Exception as e:
        print(f"Error cargando ayudantes disponibles: {e}")
        available_assistants = []

    try:
        course = get_course_by_id(course_id)
    except Exception:
        course = {}

    if not course:
        return redirect(url_for("landing.landing") + "?error=Curso no encontrado")

    try:
        id_user = int(id_user)
        nivel = int(nivel)
        id_rol = int(id_rol)
    except (TypeError, ValueError):
        return redirect(url_for("landing.landing") + "?error=No se pudo validar el permiso")
    
    print("USER SESSION:", user)
    print("id_user:", id_user)
    print("nivel:", nivel)
    print("id_rol:", id_rol)
    print("COURSE:", course)
    print("profesor_id del curso:", course.get("profesor_id"))
    print("ayudantes del curso:", course.get("ayudantes", []))

    es_superadmin = id_rol == 1

    if not es_superadmin:
        id_profesor = course.get("profesor_id")
        ayudantes = course.get("ayudantes", [])

        try:
            id_profesor = int(id_profesor)
        except (TypeError, ValueError):
            return redirect(url_for("landing.landing") + "?error=No se pudo validar el profesor del curso")

        es_profesor = id_user == id_profesor

        es_ayudante = False

        for ayudante in ayudantes:
            try:
                id_ayudante = int(ayudante.get("id_usuario"))
                if id_ayudante == id_user:
                    es_ayudante = True
            except (TypeError, ValueError, AttributeError):
                pass

        if not es_profesor and not es_ayudante:
            return redirect(url_for("landing.landing") + "?error=No tenés permiso para ver este curso")

    
    
    if request.method == 'POST':
        if request.form.get("delete_team"):
            team_id = request.form.get("delete_team")
            try:
                requests.delete(f"{BASE_URL}/equipos/{team_id}", headers=headers)
            except Exception as e:
                print(f"Error deleting team: {e}")
            return redirect(url_for('courses.course_detail', course_id=course_id, tab='teams'))
        try:
            data = {
                "nombre":   request.form.get('nombre'),
                "apellido": request.form.get('apellido'),
                "padron":   int(request.form.get('padron')),
                "correo":   request.form.get('correo'),
                "id_curso": course_id
            }
            post_student(data)
        except Exception as e:
            print(f"Error al crear alumno: {e}")

        return redirect(url_for('courses.course_detail', course_id=course_id, tab='students'))

    active_tab = request.args.get('tab', 'general')
    page       = request.args.get('page', 1, type=int)
    per_page   = 10
    order_by   = request.args.get('order_by')
    order      = request.args.get('order')

    token   = session.get('token')
    headers = {'Authorization': f'Bearer {token}'}

    assistants = []
    available_assistants = []

    try:
        assistants_res = requests.get(
            f'{BACKEND_URL}/courses/{course_id}/assistants',
            headers=headers
        )

        assistants_data = assistants_res.json() if assistants_res.ok else {}
        assistants = assistants_data.get("assistants") or assistants_data.get("data") or []

        print("STATUS ASSISTANTS:", assistants_res.status_code)
        print("JSON ASSISTANTS:", assistants_data)
        print("ASSISTANTS:", assistants)

    except Exception as e:
        print(f"Error cargando ayudantes del curso: {e}")
        assistants = []

    try:
        available_assistants_res = requests.get(
            f'{BACKEND_URL}/users',
            params={"id_rol": 3},
            headers=headers
        )

        available_assistants_data = available_assistants_res.json() if available_assistants_res.ok else {}
        available_assistants = available_assistants_data.get("users") or available_assistants_data.get("data") or []

        print("STATUS AVAILABLE ASSISTANTS:", available_assistants_res.status_code)
        print("JSON AVAILABLE ASSISTANTS:", available_assistants_data)
        print("AVAILABLE ASSISTANTS:", available_assistants)

    except Exception as e:
        print(f"Error cargando ayudantes disponibles: {e}")
        available_assistants = []

    try:
        evaluaciones = get_exams_by_course_id(course_id)
    except Exception:
        evaluaciones = []

    try:
        tipos_res      = requests.get(f'{BACKEND_URL}/tipos-evaluacion')
        tipos_evaluacion = tipos_res.json().get("exam_types", [])
    except Exception as e:
        print(f"Error loading tipos de evaluacion: {e}")
        tipos_evaluacion = []

    try:
        params = {'id_curso': course_id, 'page': page, 'per_page': per_page}
        if order_by:
            params['order_by'] = order_by
        if order:
            params['order'] = order

        students_res  = requests.get(f'{BASE_URL}/students_with_notes', params=params, headers=headers)
        response_data = students_res.json()
        students_data = response_data.get('data') or response_data.get('students') or []
        total         = response_data.get('total', len(students_data))
    except Exception:
        students_data = []
        total         = 0

    filtro_modalidad=request.args.get("modalidad")
    filtro_tipo=request.args.get("tipo")
    id_clase_editar = request.args.get("editar", type=int)
    try:
        clases_res  = requests.get(f'{BASE_URL}/clases?id_curso={course_id}')
        clases_json = clases_res.json()
        clases      = clases_json.get("classes", [])
        if filtro_modalidad:
            clases=[c for c in clases if c.get('modalidad')==filtro_modalidad]
        if filtro_tipo:
            clases=[c for c in clases if c.get('tipo')==filtro_tipo]  
    except Exception as e:
        print(e)
        clases = []
    

    for s in students_data:
        notas_dict = {}
        raw_string = s.get('notas_raw') or ""
        if raw_string:
            for par in raw_string.split(','):
                if ':' in par:
                    id_ev, nota = par.split(':', 1)
                    try:
                        key_int = int(id_ev.strip())
                        key_str = str(key_int)
                        notas_dict[key_int] = nota.strip()
                        notas_dict[key_str] = nota.strip()
                    except ValueError:
                        pass
        s['notas_todas'] = notas_dict
        s['notas_json']  = {str(k): v for k, v in notas_dict.items() if isinstance(k, int)}

        correctores_dict = {}
        raw_corr = s.get('correctores_raw') or ""
        if raw_corr:
            for par in raw_corr.split(','):
                if ':' in par:
                    id_ev, nombre_corr = par.split(':', 1)
                    try:
                        val = nombre_corr.strip()
                        if val:
                            key_int = int(id_ev.strip())
                            correctores_dict[key_int] = val
                            correctores_dict[str(key_int)] = val
                    except ValueError:
                        pass
        s['correctores_todas'] = correctores_dict

        if not s.get('promedio_final') and notas_dict:
            valores = [float(v) for k, v in notas_dict.items() if isinstance(k, int) and v not in ('', None)]
            s['promedio_final'] = round(sum(valores) / len(valores), 1) if valores else None

    eval_id_sel    = session.get('eval_seleccionada')
    eval_seleccionada = next((e for e in evaluaciones if e['id_evaluacion'] == eval_id_sel), None)
    if not eval_seleccionada and evaluaciones:
        eval_seleccionada = evaluaciones[0]

    promedio_eval = 0.0
    if eval_seleccionada:
        notas_activa = []
        for s in students_data:
            n = s.get('notas_todas', {}).get(eval_seleccionada['id_evaluacion'])
            if n not in (None, ''):
                try:
                    notas_activa.append(float(n))
                except ValueError:
                    pass
        promedio_eval = round(sum(notas_activa) / len(notas_activa), 1) if notas_activa else 0.0

    todos_los_valores = []
    for s in students_data:
        for k, nota in (s.get('notas_todas') or {}).items():
            if isinstance(k, int) and nota not in (None, ''):
                try:
                    todos_los_valores.append(float(nota))
                except ValueError:
                    pass
    promedio_general = round(sum(todos_los_valores) / len(todos_los_valores), 1) if todos_los_valores else 0.0

    total_pages = max(1, (total + per_page - 1) // per_page)

    try:
        teams_res = requests.get(f'{BASE_URL}/equipos?id_curso={course_id}', headers=headers)
        teams_json = teams_res.json()
        teams = teams_json.get("teams") or teams_json.get("data") or []
    except Exception as e:
        print(f"Error loading teams: {e}")
        teams = []

    try:
        promo_res  = requests.get(f'{BASE_URL}/cursos/{course_id}/promocion', headers=headers)
        promo_data = promo_res.json().get('config', {})
        curso_es_promocionable  = promo_data.get('es_promocionable', False)
        curso_cuenta_asistencia = promo_data.get('cuenta_asistencia', False)
        curso_pct_asistencia    = float(promo_data.get('porcentaje_asistencia', 75.0))
        promo_evals  = promo_data.get('evaluaciones', [])
        promo_config = {}
        for p in promo_evals:
            promo_config[p['id_evaluacion']] = {
                'cuenta':      bool(p.get('cuenta_para_promocion')),
                'nota_minima': p.get('nota_minima')
            }
    except Exception:
        curso_es_promocionable  = False
        curso_cuenta_asistencia = False
        curso_pct_asistencia    = 75.0
        promo_config            = {}

    pending_team_change = session.get("pending_team_change")

    source = request.args.get("source", "all")

    try:
        if source == "panel":
            advertisements = get_advertisements_by_course(course_id)

        elif source == "slack":
            advertisements = get_slack_advertisements_by_course(course_id)

        else:
            advertisements = get_all_combined_advertisements(course_id)

    except Exception:
        advertisements = []

    try:
        dash_res  = requests.get(f'{BASE_URL}/cursos/{course_id}/dashboard', headers=headers)
        dash_data = dash_res.json().get('dashboard', {}) if dash_res.ok else {}
    except Exception:
        dash_data = {}

    try:
        asist_detalle = dash_data.get("asistencia_detalle", [])
        pct_map = {row["id_alumno"]: row["porcentaje"] for row in asist_detalle}
        for s in students_data:
            s["pct_asistencia"] = pct_map.get(s["id_alumno"], "")
    except Exception as e:
        print(f"Error adjuntando asistencia a alumnos: {e}")
        for s in students_data:
            s["pct_asistencia"] = ""

    materiales = get_materials_by_course(course_id) if active_tab == 'materials' else []

    temas = []
    if active_tab == 'config' and course.get('id_materia'):
        try:
            temas_res = requests.get(f'{BACKEND_URL}/subjects/{course["id_materia"]}/temas')
            temas = temas_res.json().get("topics", []) if temas_res.ok else []
        except Exception:
            pass

    try:
        me_res = requests.get(f'{BACKEND_URL}/me', headers=headers)
        me_data = me_res.json() if me_res.ok else {}
        current_user = me_data.get('user') or me_data.get('data') or {}
        if isinstance(current_user, list):
            current_user = current_user[0] if current_user else {}
        current_user_name = f"{current_user.get('nombre', '')} {current_user.get('apellido', '')}".strip()
    except Exception:
        current_user_name = ''
    
    student_found = None
    searched_team_id = request.args.get("team_id")
    searched_padron = request.args.get("padron")
    if searched_padron:
        try:
            response = requests.get(f"{BACKEND_URL}/students", headers=headers, params={"padron": searched_padron, "id_curso": course_id})
            if response.ok:
                students = response.json().get("students", [])
                if students:
                    student_found = students[0]
        except Exception as e:
            print(f"Error buscando alumno: {e}")

    return render_template(
        'course_detail.html',
        course=course,
        students=students_data,
        teams=teams,
        student_found=student_found,
        searched_team_id=searched_team_id,
        searched_padron=searched_padron,
        clases=clases,
        filtro_modalidad=filtro_modalidad,
        filtro_tipo=filtro_tipo,
        id_clase_editar=id_clase_editar,
        active_page='courses',
        page=page,
        total_pages=total_pages,
        course_id=course_id,
        active_tab=active_tab,
        materiales=materiales,
        evaluaciones=evaluaciones,
        tipos_evaluacion=tipos_evaluacion,
        eval_seleccionada=eval_seleccionada,
        promedio_eval=promedio_eval,
        promedio_general=promedio_general,
        curso_es_promocionable=curso_es_promocionable,
        curso_cuenta_asistencia=curso_cuenta_asistencia,
        curso_pct_asistencia=curso_pct_asistencia,
        promo_config=promo_config,
        pending_team_change=pending_team_change,
        advertisements=advertisements,
        source=source,
        config_msg=session.pop('config_msg', None),
        config_ok=session.pop('config_ok', False),
        dash_data=dash_data,
        current_user_name=current_user_name,
        assistants=assistants,
        available_assistants=available_assistants,
        temas=temas,
        nivel=nivel,
    )

@courses_bp.route("/cursos/<int:course_id>/ayudantes/agregar", methods=["POST"])
def agregar_ayudante_curso(course_id):
    token = session.get("token")

    if not token:
        return redirect(url_for("landing.landing") + "?error=Debés iniciar sesión")

    id_ayudante = request.form.get("id_ayudante")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        requests.post(
            f"{BACKEND_URL}/courses/{course_id}/assistants",
            json={"id_ayudante": id_ayudante},
            headers=headers
        )
    except Exception as e:
        print(f"Error agregando ayudante al curso: {e}")

    return redirect(url_for(
        "courses.course_detail",
        course_id=course_id,
        tab="config"
    ))

@courses_bp.route("/cursos/<int:course_id>/ayudantes/<int:assistant_id>/quitar", methods=["POST"])
def quitar_ayudante_curso(course_id, assistant_id):
    token = session.get("token")

    if not token:
        return redirect(url_for("landing.landing") + "?error=Debés iniciar sesión")

    headers = {"Authorization": f"Bearer {token}"}

    try:
        requests.delete(
            f"{BACKEND_URL}/courses/{course_id}/assistants/{assistant_id}",
            headers=headers
        )
    except Exception as e:
        print(f"Error quitando ayudante del curso: {e}")

    return redirect(url_for(
        "courses.course_detail",
        course_id=course_id,
        tab="config"
    ))