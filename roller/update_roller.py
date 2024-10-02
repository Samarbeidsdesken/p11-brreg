

import requests
from dbfunctions.dbinsert_roller import insert_roller
import json
from datetime import datetime, timedelta

# Endepunkt:
# https://data.brreg.no/enhetsregisteret/api/enheter/{enhetorgnr}/roller


def get_updated_roles(maxid):

    #yesterday = datetime.now() - timedelta(lag)
    #yesterday = datetime.strftime(yesterday, format='%Y-%m-%d')
    #url = """https://data.brreg.no/enhetsregisteret/api/oppdateringer/roller?size=10000&afterTime={yesterday}T00:00:00.000Z""".format(
    #    yesterday=yesterday)
   # 
    url = """
    https://data.brreg.no/enhetsregisteret/api/oppdateringer/roller?size=10000&afterId={maxid}
    """.format(maxid = maxid)

    try:
        req = requests.get(url)
        req.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
        return req.json()

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")
    except requests.exceptions.Timeout as timeout_err:
        print(f"Timeout error occurred: {timeout_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"An error occurred: {req_err}")

    # If any exception occurs, log the orgnr to the text file

    return None  # Return None if any exception occurs


if __name__ == '__main__':
    updated_orgs = get_updated_roles()
    print(len(updated_orgs))
    # for elem in updated_orgs:
    #    print(elem)
