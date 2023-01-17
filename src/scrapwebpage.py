import requests
import src.databasehelper as db
from bs4 import BeautifulSoup
import uuid
import inflect

class ScrapWebPage():
    
    def scrap_web_page_paragraph(webpage):
        # Get the HTML from the page
        resp = requests.get(webpage)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find_all('p')
        id = 1
        p = inflect.engine()
        for row in rows:
            question = 'read paragraph ' + p.number_to_words(id) 
            db.DatabaseHelper.writeToDatabase(str(uuid.uuid4()), webpage, row, row.text, 'paragraph', question)
            id += 1 

    def scrap_web_page_title(webpage):
        # Get the HTML from the page
        resp = requests.get(webpage)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        question = 'what is the title'
        title = soup.find('title')
        db.DatabaseHelper.writeToDatabase(str(uuid.uuid4()), webpage, title, title.text, 'title', question)

    def scrap_web_page_header(webpage):
               # Get the HTML from the page
        resp = requests.get(webpage)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find_all('h2')
        id = 0
        for row in rows:
            question = 'read header ' + str(id)
            db.DatabaseHelper.writeToDatabase(str(uuid.uuid4()), webpage, row, row.text, 'header', question)
            id += 1 

    def scrap_web_page_link(webpage):
               # Get the HTML from the page
        resp = requests.get(webpage)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        rows = soup.find_all('a')
        id = 0
        for row in rows:
            question = 'read link ' + str(id)
            db.DatabaseHelper.writeToDatabase(str(uuid.uuid4()), webpage, row, row.text, 'link', question)
            id += 1 

    def scrap_web_page_source(webpage):
        # Get the HTML from the page
        resp = requests.get(webpage)
        html = resp.text
        soup = BeautifulSoup(html, 'lxml')
        text = soup.find_all(text=True)
        question = 'what is the source'
        output = ''
        blacklist = [
            '[document]',
            'noscript',
            'header',
            'html',
            'meta',
            'head', 
            'input',
            'script',
            # there may be more elements you don't want, such as "style", etc.
        ]

        for t in text:
            if t.parent.name not in blacklist:
                output += '{} '.format(t)
        formatted = output.replace('"', '')
        formattedagain = formatted.replace("\n", "")
        db.DatabaseHelper.writeToDatabase(str(uuid.uuid4()), webpage, soup, formattedagain, 'source', question)


