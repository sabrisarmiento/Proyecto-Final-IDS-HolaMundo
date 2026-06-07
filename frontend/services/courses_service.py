import requests

def get_courses():
  try:
    response = requests.get("http://localhost:5000/courses")
    response.raise_for_status()
    return response.json().get("courses", [])
  except Exception as e:
    return []
  
def get_course_by_subject(name):
  try:
    res = requests.get("http://localhost:5000/courses", params={"materia": str(name)})
    res.raise_for_status()
    return res.json().get("courses", [])
  except Exception as e:
    return {}