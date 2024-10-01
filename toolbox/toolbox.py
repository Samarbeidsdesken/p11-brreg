

# Function for parsing the addres of a company after it is returned 
# as json from the brreg API
def parse_address(dictdata):
    forretningsadresse_adresse = ''
    if 'forretningsadresse' in dictdata and 'adresse' in dictdata['forretningsadresse']:
        if isinstance(dictdata['forretningsadresse']['adresse'], list):
            forretningsadresse_adresse = ', '.join(
                dictdata['forretningsadresse']['adresse'])
        else:
            forretningsadresse_adresse = str(
                dictdata['forretningsadresse']['adresse'])

    mytuple = (
        dictdata['organisasjonsnummer'],
        forretningsadresse_adresse,
        dictdata['forretningsadresse']['postnummer'],
        dictdata['forretningsadresse']['kommunenummer'],
        dictdata['forretningsadresse']['land'],
        dictdata['forretningsadresse']['landkode']
    )
    mytuple_updated = tuple(
        None if item == '' else item for item in mytuple)

    return mytuple_updated