# csv2db

## Supported Argument
 - input: Path to the location of file or directory you want to parse
 - keepdb: If this flag specified, use existing database, otherwise insert data into new db
 - header: If this flag specified, we assume that the first row in the file are column names
```
python csv2db.py --input file/location --keepdb --header
```
