
import requests

def get_org(orgnr):

    url = 'https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}'.format(
        orgnr = orgnr
    )
    
    try:
        
        req = requests.get(url)
        print(req.json())
        
        response_dict = req.json()
        return(response_dict)
    except requests.exceptions.HTTPError as errh: 
        print("HTTP Error") 
        print(errh.args[0]) 
    except requests.exceptions.ReadTimeout as errrt: 
        print("Time out") 
    except requests.exceptions.ConnectionError as conerr: 
        print("Connection error") 
    except requests.exceptions.RequestException as errex: 
        print("Exception request")     
    
    
    