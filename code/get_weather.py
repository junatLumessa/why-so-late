import requests
from xml.etree import ElementTree
def getWeather():
    parameters = {
        'request': 'getFeature',
        'storedquery_id': 'fmi::observations::weather::daily::simple',
        'place': 'Helsinki',
        'starttime': '2016-09-07T00:00:00Z',
        'endtime': '2016-09-08T00:00:00Z'
    }
    r = requests.get('http://data.fmi.fi/fmi-apikey/' + apiKey + '/wfs', params=parameters)
    tree = ElementTree.fromstring(r.text)

    for node in tree.findall('.//{http://xml.fmi.fi/schema/wfs/2.0}BsWfsElement'):
        print(node[1].text)
        print(node[2].text)
        print(node[3].text)

getWeather()