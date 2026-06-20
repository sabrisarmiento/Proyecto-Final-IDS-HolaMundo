from config import BASE_URL
#borrar achivo

import requests

# class AdvertisementFrontendService:
#     @staticmethod
#     def get_all(id_curso=None):
def get_all_advertisements(id_curso=None):
    try:
        response = requests.get(f"{BASE_URL}/advertisements", params={"id_curso": id_curso})
        if response.status_code == 200:
            datos_api = response.json()
            return datos_api.get("advertisements", [])     
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []
        

def get_slack_advertisements():
    try:
        response = requests.get(f"{BASE_URL}/advertisements/slack")

        #print(response.status_code)
        #print(response.text)
   
        if response.status_code == 200:
            datos_api = response.json()
            return datos_api.get("advertisements", [])

        return []

    except Exception as e:
        print(f"Error: {e}")
        return []
    
def get_all_combined_advertisements(id_curso=None):
    normal_advertisements = get_all_advertisements(id_curso)
    slack_advertisements = get_slack_advertisements()

    advertisements = normal_advertisements + slack_advertisements

    return advertisements