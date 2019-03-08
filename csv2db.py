from __future__ import print_function
import os
import time
import argparse
import pandas as pd
from csvdb import CsvDB


def parse_file(filename, header):
    # read csv
    df = pd.read_csv(
        args['input'],
        header=header,
        names=[
            'date', 'instrument_parameter', 'parameter_id',
            'data_status', 'value', 'ignore'
        ]
    )

    # parse column
    df_instrument_parameter = df['instrument_parameter'].str.extract(
        '(?P<instrument>\\w+:\\s*\\w+\\s*):(?P<parameter>\\s*\\w+)'
    )
    df = pd.concat([df, df_instrument_parameter], axis=1)
    df = df.drop(['instrument_parameter'], axis=1)
    return df


if __name__ == '__main__':
    # Argument Parser
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True,
                    help='Path to the location of file or directory')
    ap.add_argument('--keepdb', action='store_true',
                    help='Keep the existing db if specified')
    ap.add_argument('--header', action='store_true',
                    help='First column is description')
    args = vars(ap.parse_args())

    db = CsvDB()

    # drop and create a new schema if keepdb flag not specified
    if not args['keepdb']:
        db.drop_all()
        db.create_all()

    start_time = time.time()
    header = 0 if args['header'] else None

    # check if the input file is file or directory
    if os.path.isdir(args['input']):
        print('Input is a directory...\nSearchiing files in this location')

    elif os.path.isfile(args['input']):
        print('Input is a single file')
        df = parse_file(args['input'], header)
    else:
        print('Invalid input')

    end_time = time.time()
    print('Elapsed time: {}'.format(end_time - start_time))
