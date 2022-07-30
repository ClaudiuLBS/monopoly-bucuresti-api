import json
from django.http import JsonResponse
from xml.etree import ElementTree

# DONT FORGET TO REMOVE xmlns="http://www.opengis.net/kml/2.2" FROM <kml> TAG

def getNeighbourhoods(request):
  dom = ElementTree.parse('Cartiere.kml').getroot()

  cartiere = []
  for item in dom.findall('Document/Placemark'):
    cartier = {}
    cartier['name'] = item.find('name').text

    coordinatesStr = item.find('Polygon/outerBoundaryIs/LinearRing/coordinates').text.replace('\t', '').replace('\n', '').split(' ')
    coordinates = []

    for point in coordinatesStr:
      if point:
        coordinates.append({
          'longitude': float(point.split(',')[0]),
          'latitude': float(point.split(',')[1])
        })
      
    cartier['coordinates'] = coordinates
    cartiere.append(cartier)

  return JsonResponse({'data': cartiere})
