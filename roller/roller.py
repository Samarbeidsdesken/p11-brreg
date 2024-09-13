# https://data.brreg.no/enhetsregisteret/api/dokumentasjon/no/index.html#tag/Roller

import requests
from dbfunctions.dbinsert_roller import insert_roller
import json

# Endepunkt:
# https://data.brreg.no/enhetsregisteret/api/enheter/{enhetorgnr}/roller


def get_company_roles(orgnr, error_log_file='error_log.txt'):
    url = f'https://data.brreg.no/enhetsregisteret/api/enheter/{orgnr}/roller'

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
    with open(error_log_file, 'a') as f:
        f.write(f"{orgnr}\n")

    return None  # Return None if any exception occurs


def get_roles(response_dict):

    try:
        if not isinstance(response_dict, dict):
            raise TypeError("Provided object is not a dictionary")

        roller = {}

        for elem in response_dict['rollegrupper']:
            #    print(elem)

            if 'roller' in elem.keys():
                for rolle in elem['roller']:

                    if 'person' in rolle.keys():

                        person_dict = {
                            'fodselsdato': rolle['person']['fodselsdato'],
                            'fornavn': rolle['person']['navn']['fornavn'],
                            'mellomnavn': rolle['person']['navn']['mellomnavn'] if 'mellomnavn' in rolle['person']['navn'].keys() else None,
                            'etternavn': rolle['person']['navn']['etternavn'],
                            'fratraadt': rolle['fratraadt'],
                            'rekkefolge': rolle['rekkefolge'],
                            'sistEndret': elem['sistEndret']
                        }

                        if rolle['type']['kode'] in roller.keys():

                            if isinstance(roller[rolle['type']['kode']], list):
                                roller[rolle['type']['kode']].append(
                                    person_dict)
                            else:
                                roller[rolle['type']['kode']] = [
                                    roller[rolle['type']['kode']], person_dict
                                ]
                        else:
                            roller[rolle['type']['kode']] = person_dict

        return roller

    except TypeError as type_err:
        print(f"Type error occurred: {type_err}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == '__main__':
    orgnr = '983609155'
    response_dict = get_company_roles(orgnr)

    print(type(response_dict))

    if response_dict:

        roller = get_roles(response_dict)

        if roller:

            data = [(orgnr, json.dumps(roller))]

            insert_roller(data)
