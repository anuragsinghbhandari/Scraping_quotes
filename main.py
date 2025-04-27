import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv
import sqlite3

#To store the data extracted
data = []

#Total 10 pages 
for i in range(1,11):

    #getting html part of quotes
    request = requests.get(f'http://quotes.toscrape.com/page/{i}/')
    soup = BeautifulSoup(request.text, 'lxml')
    
    #finding all divs containing quotes in page no. i
    quotes_div = soup.find_all('div', class_ = 'quote')

    #extracting quote, author, link and tags from each quote block one by one
    for quote_div in quotes_div:

        #quote inside (first span tag of div)
        quote = quote_div.select_one('span.text').text

        #author inside (first small tag of div)
        author = quote_div.select_one('small.author').text

        #author inside (first a tag of div)
        author_link = quote_div.select_one('a')['href']

        #add base url if not in author link
        if not author_link.startswith('http'):
            author_link = 'http://quotes.toscrape.com/' + author_link

        #getting tags
        tags_a = quote_div.find_all('a', class_ = 'tag')
        tag = []
        for a in tags_a:
            tag.append(a.text)
        
        #adding details to data list
        data.append({
            'Quote': quote,
            'Author': author,
            'About_author_link': author_link,
            'Tags': tag
        })

#storing in csv file
df = pd.DataFrame(data)
df.to_csv(f'Quotes_from_toscrape.csv', index = False)

'''
Storing in sqlite (for learning purpose)
'''

#creating connection
conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()

#create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS quotes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    Quote TEXT,
    Author TEXT,
    About_author_link TEXT,
    Tags TEXT
)
''')

#opening csv file
with open('Quotes_from_toscrape.csv', newline = '', encoding ='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        Quote = row['Quote']
        Author = row['Author']
        About_author_link = row['About_author_link']
        Tags = row['Tags']
        cursor.execute('INSERT INTO quotes (Quote, Author, About_author_link, Tags) VALUES (?, ?, ?, ?)', (Quote, Author, About_author_link, Tags))

#Commit and close
conn.commit()
conn.close()