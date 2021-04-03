from collections import namedtuple

Object = namedtuple("Object", ["id", "name", "description", "create_date"])

tables = {}

tables['Objects'] = (
    'CREATE TABLE `Objects` ('
    '  `id` int(11) NOT NULL AUTO_INCREMENT,'
    '  `name` varchar(50) NOT NULL,'
    '  `description` varchar(500),'
    '  `create_date` date NOT NULL,'
    '  PRIMARY KEY (`id`)'
    ') ENGINE=InnoDB'
)

add_object = (
    'INSERT INTO Objects '
    '(name, description, create_date) '
    'VALUES ("{name}", "{description}", "{create_date}")'
)

get_objects = (
    'SELECT id, name, description, create_date FROM Objects'
)


update_object = (
  'UPDATE Objects '
  'SET name = \'{name}\', description=\'{description}\', create_date=\'{create_date}\' '
  'WHERE id = {id}'
)

delete_object = (
    'DELETE FROM Objects ' 
    'WHERE id = {id}'
)

q_select = (
    'SELECT {fields} FROM {tables} '
)

q_insert = (
    'INSERT INTO {table} '
    '({fields_names}) '
    'VALUES ({fields_values})'
)

q_update = (
  'UPDATE {table} '
  'SET {fields_map} '
)

q_delete = (
    'DELETE FROM {table} ' 
)

q_filter = (
    'WHERE {fields_map} '
)

