import requests

def get_courses():
  try:
    response = requests.get("http://localhost:5000/courses")
    response.raise_for_status()
    return response.json().get("courses", [])
  except Exception as e:
    return []