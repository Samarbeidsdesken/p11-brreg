import requests

# https://www.brreg.no/produkter-og-tjenester/apne-data/register-offentlig-stotte/api/

#url = 'https://data.brreg.no/rofs/od/rofs/stottetildeling/search'

url = 'https://data.brreg.no/rofs/od/rofs/stottetildeling/search?language=nob&fraDato=2024-06-01&tilDato=2024-07-01'

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
print(response_dict[1])
print(len(response_dict))