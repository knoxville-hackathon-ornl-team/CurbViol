#!/usr/bin/env python3
"""
    Used to create LaTeX output for a postcard from a database.  This creates
    two pages for a 3.5" x 5" postcard for each violation.



"""
import psycopg2
from pprint import pprint


import cardlatex


if __name__ == '__main__':
    conn = psycopg2.connect("postgresql://docker:docker@localhost:25432/gis")
    conn.set_session(autocommit=True)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM violators')

    results = cursor.fetchall()

    for result in results:
        pprint(result)


