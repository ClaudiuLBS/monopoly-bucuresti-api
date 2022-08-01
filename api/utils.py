from .models import Land

def extract_coords_from_land(land: Land):
  coordinates = [
    (
      float(x.split(',')[0]), 
      float(x.split(',')[1])
    ) for x in land.coordinates.split((' ')) 
      if len(x.split(',')) == 2
  ]
  return coordinates