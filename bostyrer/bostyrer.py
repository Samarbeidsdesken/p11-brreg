
import requests
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString, Tag
from datetime import datetime


def collect_bostyrer(orgnr, dato, type, url):
    
    # Making a GET request 
    r = requests.get(url) 
    
    # check status code for response received 
    # success code - 200 


    html = r.text
    soup = bs(html, "lxml")
    spans = soup.find_all('span')
    text = 'Krav i boet'
    try:
        
        for span in spans:
            if span.text == text:
                content = ''
                prev_span = span
                text = []
                while content != '.':
                    next_span = prev_span.find_next('span')
                    text.append(next_span.next_sibling)
                    content = next_span.text
                    #print(text)
                    prev_span = next_span

        text = [item for item in text if item is not None]
        data = (
            orgnr, 
            dato,
            type,
            text[1], 
            text[2], 
            text[4], 
            text[6].text, 
            datetime.strptime(text[7], '%d.%m.%Y').date(), 
            datetime.strptime(text[9], '%d.%m.%Y').date()
            )
        #bostyrer = {
        #    'bostyrer': text[1],
        #    'gateadresse': text[2],
        #    'poststed': text[4],
        #    'epost': text[6].text,
        #    'frist': text[7],
        #    'fristdag': text[9],
        #}
        
        return data
    except:
        None
    
if __name__ == '__main__':
    data = collect_bostyrer('913566084', '2024-08-29', 'Tvangsoppløsning', 'https://w2.brreg.no/kunngjoring/hent_en.jsp?kid=20240000860548&sokeverdi=987327170&spraak=nb')
    print(data)
    
    