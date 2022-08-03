from .models import Land
import requests

def extract_coords_from_land(land: Land):
  coordinates = [
    (
      float(x.split(',')[0]), 
      float(x.split(',')[1])
    ) for x in land.coordinates.split((' ')) 
      if len(x.split(',')) == 2
  ]
  return coordinates

def send_push_notification(token:str, title:str, content:str):
  notification = {
    "to": token,
    "title": title,
    "body": content
  }
  r = requests.post(url='https://exp.host/--/api/v2/push/send', json=notification)

  return r.ok
