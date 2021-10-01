from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument('--incognito')
options.add_argument('--headless')
driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

def get_player_number():
    
    for gameplay_item in gameplay_items:
        try:

            first_span = gameplay_item.find('span')
            if first_span['ng-if'] == '::geekitemctrl.geekitem.data.item.minplayers > 0 || geekitemctrl.geekitem.data.item.maxplayers > 0':
                children = first_span.find_all('span')
                min_players = children[0].text.strip()
                if len(children) > 1:
                    max_players = children[1].text.strip()[1]
                    return min_players, max_players
                else:
                    return min_players, min_players
        except:

            continue

def get_weight():
    
    for gameplay_item in gameplay_items:
        try:

            second_span = gameplay_item.find_all('span')[1]
            if second_span['ng-show'] == 'geekitemctrl.geekitem.data.item.polls.boardgameweight.votes > 0':
                return second_span.find('span').text.strip()
        except:

            continue

def get_designers():

    for outline_item in outline_items:
        if outline_item.find('div').find('a')['name'] == 'boardgamedesigner':
            designers = outline_item.find('div', class_ = 'outline-item-description').find('div')
            break
    
    designer_list = []
    designers = designers.find_all('a')
    for i in range(len(designers)):
        designer_list.append(designers[i].text.strip())
    
    return designer_list

def get_categories():
    
    for outline_item in outline_items:
        if outline_item.find('div').find('a')['name'] == 'boardgamecategory':
            categories = outline_item.find('div', class_ = 'outline-item-description').find('div')
            break
    
    category_list = []
    categories = categories.find_all('a')
    for i in range(len(categories)):
        category_list.append(categories[i].text.strip())
    
    return category_list

def get_mechanics():
    
    for outline_item in outline_items:
        if outline_item.find('div').find('a')['name'] == 'boardgamemechanic':
            mechanics = outline_item.find('div', class_ = 'outline-item-description').find('div')
            break
    
    mechanic_list = []
    mechanics = mechanics.find_all('a')
    for i in range(len(mechanics)):
        mechanic_list.append(mechanics[i].text.strip())
    
    return mechanic_list

def get_reimplements():
    reimplements_URL = game_URL + '/linkeditems/reimplements'
    driver.get(reimplements_URL)
    reimplements_page = driver.page_source
    reimplements_soup = BeautifulSoup(reimplements_page, 'html.parser')

    toolbar_count = reimplements_soup.find('div', class_ = 'panel-body-toolbar-count')
    try:

        if toolbar_count.parent.parent.find('div', class_ = 'text-muted').text.strip() == 'No items found.':
            return []
    except:
        
        pass
    reimplements_number = int(toolbar_count.find('span').contents[-2].text.strip())
    reimplements_list = []

    for i in range(((reimplements_number - 1) // 10) + 1):

        if i > 0:
            driver.get(reimplements_URL + '?pageid=' + str(i + 1))
            reimplements_page = driver.page_source
            reimplements_soup = BeautifulSoup(reimplements_page, 'html.parser')
        
        summary_items = reimplements_soup.find_all('li', class_ = 'summary-item')
        for summary_item in summary_items:
            reimplements_list.append(summary_item.find('div', class_ = 'summary-item-title').find('a').text.strip())
                
    return str(reimplements_list)

def get_reimplemented_by():
    reimplemented_by_URL = game_URL + '/linkeditems/reimplementedby'
    driver.get(reimplemented_by_URL)
    reimplemented_by_page = driver.page_source
    reimplemented_by_soup = BeautifulSoup(reimplemented_by_page, 'html.parser')

    toolbar_count = reimplemented_by_soup.find('div', class_ = 'panel-body-toolbar-count')
    try:

        if toolbar_count.parent.parent.find('div', class_ = 'text-muted').text.strip() == 'No items found.':
            return []
    except:

        pass
    reimplemented_by_number = int(toolbar_count.find('span').contents[-2].text.strip())

    reimplemented_by_list = []

    for i in range(((reimplemented_by_number - 1) // 10) + 1):

        if i > 0:
            driver.get(reimplemented_by_URL + '?pageid=' + str(i + 1))
            reimplemented_by_page = driver.page_source
            reimplemented_by_soup = BeautifulSoup(reimplemented_by_page, 'html.parser')
        
        summary_items = reimplemented_by_soup.find_all('li', class_ = 'summary-item')
        for summary_item in summary_items:
            reimplemented_by_list.append(summary_item.find('div', class_ = 'summary-item-title').find('a').text.strip())
    
    return str(reimplemented_by_list)

title_df = pd.read_csv('bgg_titles.csv')
main_df = pd.DataFrame(data = None, columns = ['Title', 'Geek Rating', 'Link', 'Min Player No.', 'Max Player No.', 'Weight', 'Designers', 'Categories', 'Mechanics', 'Reimplements', 'Reimplemented by'])
main_df.to_csv('bgg_data.csv')

for page in range(100):

    title_data = title_df[page * 100 : (page + 1) * 100].to_numpy()
    df_data = []

    i = 0
    n_tries = 0
    fill_list = ['', '', '', '', '', '', '', '']

    while i < 100:

        game_data = []

        try:

            if n_tries == 10:
                for x in fill_list:
                    game_data.append(x)
            else:
                game_URL = title_df['Link'][100*page + i]
                driver.get(game_URL)
                game_page = driver.page_source
                game_soup = BeautifulSoup(game_page, 'html.parser')

                gameplay_items = game_soup.find_all('div', class_ = 'gameplay-item-primary')
                min_players, max_players = get_player_number()
                game_data.append(min_players)
                game_data.append(max_players)
                game_data.append(get_weight())

                credit_URL = game_URL + '/credits'
                driver.get(credit_URL)
                credit_page = driver.page_source
                credit_soup = BeautifulSoup(credit_page, 'html.parser')

                outline_items = credit_soup.find_all('li', class_ = 'outline-item')        
                game_data.append(get_designers())
                game_data.append(get_categories())
                game_data.append(get_mechanics())

                game_data.append(get_reimplements())
                game_data.append(get_reimplemented_by())

            df_data.append(game_data)
            i += 1
            n_tries = 0
        
        except:

            n_tries += 1
            continue
        
    main_data = np.c_[title_data, df_data]
    main_df = pd.DataFrame(data = main_data, columns = ['Title', 'Geek Rating', 'Link', 'Min Player No.', 'Max Player No.', 'Weight', 'Designers', 'Categories', 'Mechanics', 'Reimplements', 'Reimplemented by'])
    main_df.to_csv('bgg_data.csv', mode='a', header=False)