from __future__ import print_function
import argparse
from csvdb import CsvDB


# Argument Parser
ap = argparse.ArgumentParser()
ap.add_argument("-k", "--keepdb", action='store_true',
                help='Keep the existing db if specified')
args = vars(ap.parse_args())

db = CsvDB()

if not args['keepdb']:
    db.drop_all()
    db.create_all()


