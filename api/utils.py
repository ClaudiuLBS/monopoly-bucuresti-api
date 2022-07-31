from .models import Neighbourhood

def extract_coords_from_neighbourhood(neighboorhood: Neighbourhood):
  coordinates = [
    (
      float(x.split(',')[0]), 
      float(x.split(',')[1])
    ) for x in neighboorhood.coordinates.split((' ')) 
      if len(x.split(',')) == 2
  ]
  return coordinates