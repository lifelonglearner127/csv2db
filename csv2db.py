from __future__ import print_function
import os
import time
import conf
import argparse
import pandas as pd
import mysql.connector
from mysql.connector import errorcode


def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS {} DEFAULT CHARACTER SET 'utf8'"
            .format(conf.DB_NAME)
        )
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


def drop_database(cursor):
    try:
        cursor.execute(
            "DROP DATABASE IF EXISTS {}".format(conf.DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)


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

    start_time = time.time()

    # connect mysql server
    cnx = mysql.connector.connect(
        host=conf.HOST,
        user=conf.USER,
        passwd=conf.PASSWD
    )
    cursor = cnx.cursor()

    # drop the database
    if not args['keepdb']:
        drop_database(cursor)
        print("Database {} dropped successfully.".format(conf.DB_NAME))

    # use database; if not exists create databases
    try:
        cursor.execute("USE {}".format(conf.DB_NAME))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(conf.DB_NAME))
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(conf.DB_NAME))
            cnx.database = conf.DB_NAME
        else:
            print(err)
            exit(1)

    # create tables
    for table_name in conf.TABLES:
        table_description = conf.TABLES[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    header = 0 if args['header'] else None

    # check if the input file is file or directory
    if os.path.isdir(args['input']):
        print('Input is a directory...\nSearchiing files in this location')

    elif os.path.isfile(args['input']):
        print('Input is a single file')
        df = parse_file(args['input'], header)

    else:
        print('Invalid input')

    cursor.close()
    cnx.close()

    end_time = time.time()
    print('Elapsed time: {}'.format(end_time - start_time))
