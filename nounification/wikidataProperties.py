import requests
import json
import pickle

default_language = 'en'

def buildWikidataProperties():
    """
        Return the set of all Wikidata properties.
    """
    properties = set()
    maxRange=60
    for i in range(0,maxRange):
        print("%d/%d"%(i+1,maxRange))
        propertiesIDs = '|'.join(['P%d'%x for x in range(50*i+1,50*(i+1)+1)])
        request = requests.get('http://www.wikidata.org/w/api.php',params={'action':'wbgetentities', 'sites':'itwiki', 'ids':propertiesIDs, 'format':'json'})
        j = request.json()
        if j['success'] == 0:
            continue
        for prop in j['entities'].values():
            if 'missing' in prop.keys():
                continue
            try:
                for alias in prop['aliases'][default_language]:
                    properties.add(alias['value'])
            except KeyError: # no alias
                pass
            properties.add(prop['labels'][default_language]['value'])
    return properties

if __name__ == "__main__":
    properties = buildWikidataProperties()
    f = open('wikidataProperties.pickle', 'wb')
    pickle.dump(properties,f)
    f.close()
