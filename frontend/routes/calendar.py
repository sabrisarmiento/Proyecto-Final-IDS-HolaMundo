from flask import Blueprint, render_template
from services.calendar_frontend_service import CalendarFrontendService

calendar_bp = Blueprint('calendar', __name__)

@calendar_bp.route('/cronograma', methods=['GET'])
def calendar():
    clases_api = CalendarFrontendService.get_all()
    
    schedule = {}
    for clase in clases_api:
        week_num = clase.get('semana')
        if week_num is not None:
            # 1. Si la semana no está en el diccionario, la creamos como lista vacía
            if week_num not in schedule:
                schedule[week_num] = []
            
            # 2. REVISÁ ESTA INDENTACIÓN: Tiene que estar adentro del primer IF
            # y alineada con el segundo IF
            schedule[week_num].append(clase)

    # Armamos la lista ordenada para el HTML
    sorted_schedule = [{"week": w, "classes": schedule[w]} for w in sorted(schedule.keys())]
    
    return render_template('calendar.html', schedule=sorted_schedule)
