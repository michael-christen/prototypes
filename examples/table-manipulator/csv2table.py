import csv
import sys

from collections import defaultdict


def format_row(row, column2max):
    output = '|'
    for i, value in enumerate(row):
        format_str = ' {:<' + str(column2max[i]) + '} |'
        output += format_str.format(value.strip())
    return output


def format_header(row, column2max):
    output = format_row(row, column2max)
    output += '\n'
    sep_row = ['-'*column2max[i] for i in xrange(len(row))]
    output += format_row(sep_row, column2max)
    return output


def main():
    table_reader = csv.reader(sys.stdin)
    column2max = defaultdict(int)
    rows = list(table_reader)
    for row in rows:
        print ', '.join(row)
        for i, value in enumerate(row):
            column2max[i] = max(column2max[i], len(value.strip()))
    print column2max
    output = ''
    for i, row in enumerate(rows):
        if not row:
            continue
        if i == 0:
            output += format_header(row, column2max)
        else:
            output += format_row(row, column2max)
        output += '\n'
    print output


if __name__ == '__main__':
    main()
