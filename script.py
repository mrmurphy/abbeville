import os
import sqlite3
from bs4 import BeautifulSoup

# Open the HTML file relative to the script
html_file = os.path.join(os.path.dirname(__file__), 'old.html')
with open(html_file, 'r') as f:
    content = f.read()

# Parse the first HTML table
soup = BeautifulSoup(content, 'html.parser')
# Find the table with the ID 'maindata'
table = soup.find('table', id='maindata')

# Create a new SQLite database and table
conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS complaints (
        id INTEGER PRIMARY KEY,
        name_of_complainer TEXT,
        name_of_complained_against TEXT,
        box_number INTEGER,
        pack_number INTEGER,
        year INTEGER,
        type_of_document TEXT,
        abstract_of_contents TEXT
    )
''')

# Set up full text search index on all text columns
cursor.execute('''
    CREATE VIRTUAL TABLE IF NOT EXISTS complaints_fts USING fts5(
        name_of_complainer,
        name_of_complained_against,
        type_of_document,
        abstract_of_contents,
        content=complaints,
        content_rowid=id
    )
''')

# Insert every row from the HTML table into the SQLite table
for row in table.find_all('tr'):
    data = [td.get_text(strip=True) for td in row.find_all('td')][0:7]
    cursor.execute('''
        INSERT INTO complaints (
            name_of_complainer,
            name_of_complained_against,
            box_number,
            pack_number,
            year,
            type_of_document,
            abstract_of_contents
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)

# Commit the changes and close the database connection
conn.commit()
conn.close()
