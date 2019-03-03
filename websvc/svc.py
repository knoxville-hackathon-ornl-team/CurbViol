
from flask import Flask, request, send_from_directory

import psycopg2
import pprint

pp = pprint.PrettyPrinter(indent=4)

conn = psycopg2.connect("postgresql://docker:docker@localhost:25432/gis")
conn.set_session(autocommit=True)
cur1 = conn.cursor()
cur2 = conn.cursor()

app = Flask(__name__, static_url_path='')

@app.route('/index.html')
def root():
    return send_from_directory('', 'index.html')

@app.route('/style.css')
def root_css():
    return send_from_directory('', 'style.css')

@app.route('/submit', methods=['POST'])
def submit():
    cur1.execute('INSERT INTO violations("DATE", "HOUSE #", "STREET") VALUES (CURRENT_DATE, %s, %s)', (request.args.get('address','unknown'),request.args.get('details')))
    return "Updated"

@app.route('/worst', methods=['GET'])
def worst():
    cur1.execute('SELECT trim("HOUSE #") || \' \' ||  trim("STREET") as address, count(*) as offences from violations group by 1 order by 2 desc limit 10')
    return pp.pformat(cur1.fetchall())

@app.route('/geocode', methods=['PATCH'])
def geocode():
    cur1.execute('SELECT address FROM violators WHERE NOT gcattempt')
    for r in cur1:
        g = geocoder.osm(r[0])
        if g.ok:
            cur2.execute("UPDATE violators SET (lat, lon, gcattemp) = (%s, %s, %s, true)", (g.y, g.x, g.postal))
    return "Geocode complete"

