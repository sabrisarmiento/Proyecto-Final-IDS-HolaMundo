import requests

def calendar_get_all(id_curso=None):
  try:
    params = {}
    if id_curso:
      params["id_curso"] = id_curso
    response = requests.get(
      'http://localhost:5000/clases',
      params=params
    )
    if response.status_code == 200:
      return response.json().get("classes", [])
    return []

  except Exception as e:
    print(f"Error: {e}")
    return []
  
def get_schedule_by_subject(subject_id):
    try:
        response = requests.get(f"http://localhost:5000/clases/materia/{subject_id}")
        response.raise_for_status()
        return response.json().get("classes", [])
    except Exception as e:
        print(f"Error al obtener el cronograma de la materia {subject_id}: {e}")
        return []
