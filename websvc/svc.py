
from flask import Flask, request, send_from_directory

import psycopg2
import pprint
import re

pp = pprint.PrettyPrinter(indent=4)

conn = psycopg2.connect("postgresql://docker:docker@localhost:25432/gis")
conn.set_session(autocommit=True)
cur1 = conn.cursor()
cur2 = conn.cursor()

app = Flask(__name__, static_url_path='')

@app.route('/index.html')
@app.route('/')
def root():
    return send_from_directory('', 'index.html')

@app.route('/style.css')
def root_css():
    return send_from_directory('', 'style.css')

addre = r"^\s*(\d+)\s+(.+)"

@app.route('/submit', methods=['POST'])
def submit():
    print(request.form)
    m = re.search(addre, request.args.get('address', 'unknown'))
    if m:
        print('m', m.group(1), m.group(2))
        cur1.execute('INSERT INTO violations("DATE", "HOUSE #", "STREET", "DETAILS") VALUES (CURRENT_DATE, %s, %s)', (m.group(1), m.group(2), ", ".join([request.args.get("violation", "None"), request.args.get('details', "None")])))
        return "Updated"
    else:
        return "Malformed address"

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

@app.route('/stats', methods=['GET'])
def stats():
    cur1.execute('select \'OVER FLOW\' as type, count(*) from violations where "OVER FLOW" is not null UNION select \'NOT OUT\', count(*) from violations where "NOT OUT" is not null UNION select \'NOT AT CURB\', count(*) from violations where "NOT AT CURB" is not null UNION select \'Other\', count(*) from violations where "NOT OUT" is null and "NOT AT CURB" is null and "OVER FLOW" is null and "DETAILS" is not null')
    return pp.pformat(cur1.fetchall())

