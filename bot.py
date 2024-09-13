import konkurser.konkurser as konkurser
import enheter.alle_enheter as alle_enheter
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO

page_source = konkurser.scrape_announcements('30.05.2024', '31.05.2024')
soup = bs(page_source, 'html.parser')
tables = soup.find_all('table')

df = konkurser.parse_table(tables[3])


df = konkurser.clean_announcements(df)
# print(df)

# enhet = virksomheter.get_org('918873724')

# for val, key in enhet.items():
#    print(str(val) + ': ' + str(key))

for orgnr in df['orgnr']:
    alle_enheter.get_org(orgnr)
