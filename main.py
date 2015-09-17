import argparse
import os
from os.path import isdir, join as pjoin
import sys
import csv

from xlsx import Workbook

from bandoc.excel import Parser
from bandoc.processor import Processor

ERR_IO = 101


def main():
    parser = argparse.ArgumentParser(description='Process data.')
    parser.add_argument('input_dir', type=str, help='folder containing input data')
    args = parser.parse_args()

    if not isdir(args.input_dir):
        print 'No such directory %r' % args.input_dir
        exit(ERR_IO)

    writer = csv.writer(sys.stdout, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    def predicate(fname):
        return fname.endswith('.xlsx')

    for fname in filter(predicate, os.listdir(args.input_dir)):
        region, res = consume_file(pjoin(args.input_dir, fname))
        writer.writerow([
            fname,
            region[0] + 1,
            region[1] + 1,
            res['q1'],
            res['q2'],
            res['q3'],
            res['q4'],
            res['q5'],
            res['q6'],
            res['q7'],
            res['q8'],
            res['prm']
        ])


def consume_file(path):
    book = Workbook(path)
    p = Parser(book)
    p.parse()
    region = Processor.get_max_region(p.samples())
    Processor.clip_to_region(region, p.samples())
    return region, Processor.split_avg(p.samples())


if __name__ == '__main__':
    main()
