import konkurser.konkurser as konkurser
from dbfunctions.dbinsert_konkurser import insert_konkurser
from dbfunctions.dbinsert_bostyrer import insert_bostyrer
import bostyrer.bostyrer as bostyrer
from bs4 import BeautifulSoup as bs
import pandas as pd
from io import StringIO
from datetime import datetime, timedelta
import re

# for x in range(2, 12):

yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, format='%d.%m.%Y')

# print(yesterday)

# print(str(x+1) + ': ' + str(print(yesterday)))

page_source = konkurser.scrape_announcements(yesterday, yesterday)
soup = bs(page_source, 'html.parser')
tables = soup.find_all('table')
table_rows = soup.find_all('tr')

df = pd.DataFrame()
data = []
# Loop through each table row  on the whole page
for row in table_rows:
    row_data = []

    # ignore trs that has nested tables. These function as duplicates.
    if row.find('table'):
        pass
    else:

        # Check if any td in the row has a img-tag with an onclick function of kopier_orgnr.
        has_td_img = [True if td.find(
            'img', onclick=lambda x: x and 'kopier_orgnr' in x) else False for td in row.find_all('td')]

        # If the img-tag is found, collect the data from the row.
        if any(has_td_img):
            # Loop through each td in the row
            for td in row.find_all('td'):

                row_dict = {'navn': None, 'orgnr': None,
                            'dato': None, 'type': None, 'url': None}

                # Look for img tags with the onclick function 'kopier_orgnr'
                img_tag = td.find(
                    'img', onclick=lambda x: x and 'kopier_orgnr' in x)

                # Add the text content of the td to the row data
                text_content = td.get_text(strip=True)
                if text_content:
                    row_data.append(text_content)

                # Look for a tags to extract the href attribute
                a_tag = td.find('a')
                if a_tag and 'href' in a_tag.attrs:
                    url = a_tag['href']
                    row_data.append(
                        f'https://w2.brreg.no/kunngjoring/{url}')

            # Print the row data if it contains relevant information
            if row_data:

                row_dict['navn'] = row_data[0]

                orgnnr = re.sub("[^0-9]", "", row_data[1])
                row_dict['orgnr'] = orgnnr
                row_dict['dato'] = yesterday
                # row_dict['dato'] = row_data[2]
                row_dict['type'] = row_data[2]
                row_dict['url'] = row_data[3]

                data.append(row_dict)

df = pd.DataFrame(
    data, columns=['navn', 'orgnr', 'dato', 'type', 'url'])
df['dato'] = pd.to_datetime(df['dato'], format='%d.%m.%Y')

# print(df)

konkurser = []
for row in df.itertuples(name=None, index=False):

    insert_konkurser([row])

    bostyrer_data = bostyrer.collect_bostyrer(
        orgnr=row[1], dato=row[2], type=row[3], url=row[4])

    if bostyrer_data:
        # print('bostyrer')
        insert_bostyrer([bostyrer_data])
    # konkurser.append(row)

#

# df.to_excel('konkurser.xls
