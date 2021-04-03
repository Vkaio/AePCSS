from flask import current_app, g
from flask.cli import with_appcontext
import mysql.connector
from .model import tables

user='dev'
password='password'
host='localhost'
database='dbtest'

def get_db():
    if 'db' not in g:
        g.db = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    cursor = get_db().cursor()

    for table in tables:
        table_decription = tables[table]

        cursor.execute(f'DROP TABLE IF EXISTS `{table}`')

        try:
            print(f'Creating the {table} table...', end=' ')
            cursor.execute(table_decription)
        except mysql.connector.Error as err:
            print(err.msg)
        else:
            print('Ok')

    close_db()


def init_app(app):
    app.teardown_appcontext(close_db)