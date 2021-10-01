import requests
from bs4 import BeautifulSoup
import pandas as pd

def get_title(html):
    
    return html.find('a', class_ = 'primary').text.strip()

def get_geek_rating(html):
    
    return html.find('td', class_ = 'collection_bggrating').text.strip()

def get_pagelink(html):

    return 'https://boardgamegeek.com' + html.find('a', class_ = 'primary')['href']

df_data = []

for page in range(1, 101):
    browse_URL = 'https://boardgamegeek.com/browse/boardgame/page/' + str(page)
    browse_page = requests.get(browse_URL)
    browse_soup = BeautifulSoup(browse_page.content, 'html.parser')
    
    rows = browse_soup.find_all(id = 'row_')
    
    for row in rows[:100]:
        game_data = []
        game_data.append(get_title(row))
        game_data.append(get_geek_rating(row))
        game_data.append(get_pagelink(row))
        df_data.append(game_data)

df = pd.DataFrame(df_data, columns = ['Title', 'Geek Rating', 'Link'])

df.to_csv('bgg_titles.csv', index = False)