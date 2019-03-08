HOST = 'localhost'
USER = 'name'
PASSWD = 'password'
DB_NAME = 'dbname'
TABLES = {}
TABLES['instruments'] = (
    "CREATE TABLE `instruments` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['parameters'] = (
    "CREATE TABLE `parameters` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `name` varchar(30) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['data'] = (
    "CREATE TABLE `data` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `parameter_id` int(11) NOT NULL,"
    "  `value` float(11) NOT NULL,"
    "  `to_date` date NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")

TABLES['datastatus'] = (
    "CREATE TABLE `datastatus` ("
    "  `id` int(11) NOT NULL AUTO_INCREMENT,"
    "  `datum_id` int(11) NOT NULL,"
    "  `status_id` int(11) NOT NULL,"
    "  PRIMARY KEY (`id`)"
    ") ENGINE=InnoDB")
