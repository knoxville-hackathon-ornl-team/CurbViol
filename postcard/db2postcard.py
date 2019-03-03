#!/usr/bin/env python3
"""
    Used to create LaTeX output for a postcard from a database.  This creates
    two pages for a 3.5" x 5" postcard for each violation.



"""
from pathlib import Path
import argparse
import psycopg2
from pprint import pprint


import cardlatex


def none2empty(s):
    """
    :param s: a database field value that could be none
    :return: Any none values are converted to empty strings
    """
    if s is None:
        return ''
    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a postcard LaTeX file')

    parser.add_argument('--out-file', '-o', help='Where to write the LaTeX')
    parser.add_argument('--threshold', '-t', type=int, default=3, help='Threshold for number of violations to merit a postcard')

    args = parser.parse_args()



    conn = psycopg2.connect("postgresql://docker:docker@localhost:25432/gis")
    conn.set_session(autocommit=True)

    cursor = conn.cursor()

    cursor.execute('SELECT * FROM violators')

    results = cursor.fetchall()

    # Aggregate the violations into a single dictionary keyed by concatenating the house
    # number and street name
    aggregated_violations = {}

    for result in results:
        # pprint(result)
        house_address = result[1] + result[2] # street number of street name as key

        single_address = aggregated_violations.setdefault(house_address, [])

        violation = {'DATE' : str(result[0]),
                     'HOUSE #' : result[1],
                     'STREET' : result[2],
                     'OVER FLOW' : none2empty(result[3]),
                     'NOT OUT' : none2empty(result[4]),
                     'NOT AT CURB' : none2empty(result[5]),
                     'DETAILS' : none2empty(result[6])}

        # Accumulation this violation
        single_address.append(violation)

    # Now let's cook those down to violators that exceed the given threshold
    viable_violations = {key:value for key, value in aggregated_violations.items() if len(value) > args.threshold}

    print('Considering ', len(viable_violations), 'violations out of', len(aggregated_violations), 'violations using a threshold of', args.threshold)

    # Now blat out the LaTeX for waste management violation postcards
    with Path(args.out_file).open('w') as latex_postcards_file:
        cardlatex.write_latex_preamble(latex_postcards_file)

        for viable_violation in viable_violations.values():
            cardlatex.process_violation(viable_violation, latex_postcards_file)

        cardlatex.write_latex_end(latex_postcards_file)


