import sqlite3
from jinja2 import Template

# Read the SQLite table
conn = sqlite3.connect('complaints.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM complaints')
rows = cursor.fetchall()
conn.close()

# Read the template file
with open('template.html', 'r') as f:
    template_content = f.read()

# Render the static HTML page with the template and data
template = Template(template_content)
html = template.render(rows=rows)

# Save the rendered HTML to a file
with open('index.html', 'w') as f:
    f.write(html)
