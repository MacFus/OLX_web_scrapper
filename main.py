from bs4 import BeautifulSoup
from requests import get
import pandas as pd

url = 'https://www.olx.pl/nieruchomosci/mieszkania/wynajem/malopolskie/?search%5Bfilter_enum_rooms%5D%5B0%5D=one'
locations = []
prices = []
titles = []

def parse_price(price):
    return float(price.replace(' ','').replace('zł','').replace(',','.'))

page = get(url)
bs = BeautifulSoup(page.content, 'html.parser')
for offer in bs.find_all('div', class_='offer-wrapper'):
    footer = offer.find('td', class_='bottom-cell')
    location = footer.find('small', class_='breadcrumb').get_text().strip().split(',')[0]
    title = offer.find('strong').get_text().strip()
    price = parse_price(offer.find('p', class_='price').get_text().strip())
    locations.append(location)
    prices.append(price)
    titles.append(title)
data = {'location':locations, 'title':titles, 'price':prices}
df = pd.DataFrame(data)
df.to_excel('df.xlsx', sheet_name='Pierwszy')
print(df)

