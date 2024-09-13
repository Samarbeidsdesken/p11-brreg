import requests

#url = 'https://data.brreg.no/rofs/od/rofs/stottetildeling/search'

#https://data.brreg.no/regnskapsregisteret/regnskap/swagger-ui/swagger-ui/index.html

url = 'https://data.brreg.no/regnskapsregisteret/regnskap/983609155'

data = {
    'Language': 'no',
    'fraDato': '2016-07-30',
    'tilDato': '2017-12-01'
    
}

#req = requests.get(url, params = data)
req = requests.get(url)

print(req.status_code)

# Convert json into dictionary 
response_dict = req.json()
print(response_dict)
#print(len(response_dict))