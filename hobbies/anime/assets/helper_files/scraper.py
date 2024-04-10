# Web interaction
import requests
from bs4 import BeautifulSoup

# Data manipulation
import re
import pandas as pd

# Time manipulation
import time
import random

def getAnimes():
    '''
    Scrapes Anime lists from a website.
    '''

    # Lists to store the different attributes of the anime
    ranks = []
    columns = ['Episodes', 'Emition_Date', 'Users'] # Plus the ones from the website's table
    names = []
    episodes = []
    emition_date = []
    users = []
    score = []
    
    # Rank number to start scraping from (Ex: Anime ranked from 1 - 50)
    rank = 0
    for i in range(200):
        # Waits between 2 to 6 seconds before making a request on the server
        time.sleep(random.randrange(1, 3))

        # Visibility
        print(f'Scraping page number {i}')

        # Confirm we got an useful response from the server before continuing, if not, try again
        responded = False
        while not responded:
            try:
                response = requests.get(f'https://myanimelist.net/topanime.php?type=tv&limit={rank}').content
                if response == None:
                    raise Exception('No Response')
            except:
                pass
            else:
                responded = True
        
        #When a response has been confirmed, continue with the scraping
        try:
            soup = BeautifulSoup(response, 'html.parser').find('table')
            if len(columns) < 8:
                columns.extend([column.text for column in soup.select('tr td')])
            else:
                pass

            ranks.extend([rank.text for rank in soup.select('tr.ranking-list td.rank.ac span')])

            names.extend([name.text for name in soup.select('div h3 a')])

            information = [(re.sub('   +', '.', detail.text.replace('\n', ''))).split('.')[1:-1]
                    for detail in soup.select('div.information.di-ib.mt4')]
            
            episodes.extend([i[0] for i in information])

            emition_date.extend([i[1] for i in information])

            users.extend([i[2].split(' ')[0] for i in information])

            score.extend([i.text for i in soup.select('td.score.ac div span')])
        except Exception as e:
            print(str(e))
            time.sleep(5)
        else:
            rank += 50

    # Turn what we scraped into a DataFrame
    df = pd.DataFrame({col: data for col, data in zip(columns, [episodes, emition_date, users, ranks, names, score])})
    
    # Turn DataFrame into a CSV file for portability
    df.to_csv('top_animes.csv', index=False)

getAnimes()