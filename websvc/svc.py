
from flask import Flask
from flask import request

import psycopg2
import pprint

pp = pprint.PrettyPrinter(indent=4)

conn = psycopg2.connect("postgresql://docker:docker@localhost:25432/gis")
conn.set_session(autocommit=True)
cur = conn.cursor()

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit():
	cur.execute('INSERT INTO violations("DATE", "HOUSE #", "STREET") VALUES (CURRENT_DATE, %s, %s)', (request.args.get('address','unknown'),request.args.get('details')))
	return "Updated"

@app.route('/worst', methods=['GET'])
def worst():
    cur.execute('SELECT trim("HOUSE #") || \' \' ||  trim("STREET") as address, count(*) as offences from violations group by 1 order by 2 desc limit 10')
    return pp.pformat(cur.fetchall())

