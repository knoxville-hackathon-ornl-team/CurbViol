#!/usr/bin/env python3
"""
    Used to create LaTeX output for a postcard.  This prints two pages for a 3.5" x 5" postcard.
"""
import sys
import argparse
import csv
from pathlib import Path
from string import Template

# This is the script return code if we cannot open the curbside violations CSV file
NO_CSV_FILE_ERROR = 1

postcard_tex_preamble = """\\documentclass{article}

\\pagestyle{empty}
\\setlength\\parindent{0pt}
\\usepackage[paperwidth=5in,
    paperheight=3.5in,
    left=0.50in,
    right=0.50in,
    top=0.50in,
    bottom=0.50in]{geometry}

\\begin{document}
"""

postcard_tex = """
Hello, World!

This is just a little note to see how you're doing. I haven't see out since that big party in stdlib's house. I hope you've gotten out of that infinite loop I wrote after my 5th beer.

\\vfill
\\raggedleft
Your friend, \\\\
Printf

\\newpage

\\raggedright
Knoxville Solid Waste Management\\\\
400 Main St., Room 470 \\\\
Knoxville, TN 37902
\\vfill
\\centering
\\parbox{2in}{\\Large Resident\\\\
$address \\\\
Knoxville, TN 37902}
\\vfill

\\newpage
"""


postcard_tex_end = """
\\end{document}
"""


def write_latex_preamble(out_file):
    """ Write out the preamble, or start, of the LaTeX document that will contain the postcards.

    :param out_file: is the LaTeX that will contain the postcards
    :return: None
    """
    out_file.write(postcard_tex_preamble)


def write_latex_end(out_file):
    """ Write out the end of the LaTeX document for the postcards

    :param out_file: you guessed it, the LaTeX file for the postcards
    :return: None
    """
    out_file.write(postcard_tex_end)


def process_violation(violation, out_file):
    """ This will emit a corresponding postcard for the given violation to the LaTeX postcard file

    :param violation: is an OrderedDict containing details for a specific violation
    :param out_file: is an open connection to the LaTeX file
    :return: None
    """
    postcard_string = Template(postcard_tex)
    out_postcard_string = postcard_string.safe_substitute(address=violation['HOUSE #'] + ' ' + violation['STREET'])
    out_file.write(out_postcard_string)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a postcard LaTeX file')

    parser.add_argument('--in-file','-i', help='CSV file of curbside violations')
    parser.add_argument('--out-file', '-o', help='Where to write the LaTeX')

    args = parser.parse_args()

    curbside_violation_path = Path(args.in_file)

    if not curbside_violation_path.exists():
        print(violations_csv_file, 'does not exist ... exiting')
        sys.exit(NO_CSV_FILE_ERROR)

    # We've got curbside violations, so let's start writing the LaTeX that will contain all the postcards

    with Path(args.out_file).open('w') as latex_postcards_file:
        write_latex_preamble(latex_postcards_file)

        with curbside_violation_path.open('r') as curbside_violation:
            violations_reader = csv.DictReader(curbside_violation)

            for violation in violations_reader:
                process_violation(violation, latex_postcards_file)

        write_latex_end(latex_postcards_file)



