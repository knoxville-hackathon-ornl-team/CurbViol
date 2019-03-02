#!/usr/bin/env python3
"""
    Used to create LaTeX output for a postcard.
"""
import argparse
from pathlib import Path

postcard_tex = """\\documentclass{article}

\\pagestyle{empty}
\\setlength\\parindent{0pt}
\\usepackage[paperwidth=5in,
    paperheight=3.5in,
    left=0.50in,
    right=0.50in,
    top=0.50in,
    bottom=0.50in]{geometry}

\\begin{document}
Hello, World!

This is just a little note to see how you're doing. I haven't see out since that big party in stdlib's house. I hope you've gotten out of that infinite loop I wrote after my 5th beer.

\\vfill
\\raggedleft
Your friend, \\\\
Printf

\\newpage

\\raggedright
return 0; \\\\
123 Main St \\\\
Big City, ES 12345
\\vfill
\\centering
\\parbox{2in}{Mr World \\\\
123 Knuth Dr \\\\
Central Processor, UT 0x000}
\\vfill
\\end{document}"""

def write_latex(file_name):
    """
    :param file_name: to which to write the LaTeX
    :return: None
    """
    with Path(file_name).open('w') as latex_file:
        latex_file.write(postcard_tex)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate a postcard LaTeX file')

    parser.add_argument('--out-file', '-o', help='Where to write the LaTeX')

    args = parser.parse_args()

    write_latex(file_name=args.out_file)



