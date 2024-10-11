

# Function for parsing the addres of a company after it is returned 
# as json from the brreg API
def parse_address(dictdata):
    mytuple = None
    
    if 'forretningsadresse' in dictdata:
        forretningsadresse_adresse = ''
        if 'adresse' in dictdata['forretningsadresse']:
            if isinstance(dictdata['forretningsadresse']['adresse'], list):
                forretningsadresse_adresse = ', '.join(
                    dictdata['forretningsadresse']['adresse'])
            else:
                forretningsadresse_adresse = str(
                    dictdata['forretningsadresse']['adresse'])

        mytuple = (
            dictdata['organisasjonsnummer'],
            forretningsadresse_adresse,
            dictdata['forretningsadresse']['postnummer'] if 'postnummer' in dictdata['forretningsadresse'] else None,
            dictdata['forretningsadresse']['kommunenummer'] if 'kommunenummer' in dictdata['forretningsadresse'] else None,
            dictdata['forretningsadresse']['land'] if 'land' in dictdata['forretningsadresse'] else None,
            dictdata['forretningsadresse']['landkode'] if 'landkode' in dictdata['forretningsadresse'] else None
        )
        mytuple_updated = tuple(
            None if item == '' else item for item in mytuple)

    return mytuple_updated