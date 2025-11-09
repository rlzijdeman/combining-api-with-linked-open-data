# playing with apis
# 2025-11-02

# plan: to combine data from API with Linked Data
# Use case: what countries have astronauts up in the air?
# read nasa api for astronaut names
# link to wikidata and get country of birth

# (1) get data from api :)
# (2) read data as pandas df :)
# (3) add wikidata identifiers to data
# (3) new version: feed names of astronauts in query. via VALUES maybe?
# (4) present results

import requests
import pandas as pd
from SPARQLWrapper import SPARQLWrapper, JSON


# 1. get data from api
response = requests.get("http://api.open-notify.org/astros")
#print(response.status_code)

data = response.json()
#print(data) 2 columns 'craft' and 'name'

# 2. read data as pandas df
df = pd.json_normalize(data, 'people')

print("The data from the NASI API is:\n", df, 
      "\n\nFrom what countries are these astronauts you ask?\n", 
      "that data we can retrieve from Wikidata... \n")

# 3. list names for sparql query
names = '" "'.join(df['name'])
names = '"'+ names +'"'

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
sparql.setQuery("""                                                                                                                                                  
SELECT distinct ?astronaut ?astronautLabel ?countryCitizenLabel WHERE {
  ?astronaut wdt:P106 wd:Q11631;
             rdfs:label ?astronautLabel .
  FILTER(LANG(?astronautLabel) = "en").
  FILTER(CONTAINS(?astronautLabel, ?astronautSpace )) .
  VALUES ?astronautSpace { """ + names + """ }

  OPTIONAL {
    ?astronaut wdt:P27 ?countryCitizen .
    ?countryCitizen rdfs:label ?countryCitizenLabel 
    FILTER(LANG(?countryCitizenLabel) = "en") } .
 
  SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
} ORDER BY ?countryCitizenLabel
""")

sparql.setReturnFormat(JSON)
results = sparql.query().convert()

# 4 print(results)

for result in results["results"]["bindings"]:
    print("# " + result["astronautLabel"]["value"])
    print("Country: " + result["countryCitizenLabel"]["value"])
    print("More info: " + result["astronaut"]["value"])
    print("\n")

# MISSION ACCOMPLISHED!
