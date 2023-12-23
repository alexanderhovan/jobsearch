import os
import pymysql
from flask import jsonify

db_user = os.environ.get('CLOUD_SQL_USERNAME')
db_password = os.environ.get('CLOUD_SQL_PASSWORD')
db_name = os.environ.get('CLOUD_SQL_DATABASE_NAME')
db_connection_name = os.environ.get('CLOUD_SQL_CONNECTION_NAME')

def open_connection():
    unix_socket = '/cloudsql/{}'.format(db_connection_name)
    try:
        if os.environ.get('GAE_ENV') == 'standard':
            conn = pymysql.connect(user=db_user,
                                   password=db_password,
                                   unix_socket=unix_socket,
                                   db=db_name,
                                   cursorclass=pymysql.cursors.DictCursor
                                   )
    except pymysql.MySQLError as e:
        return e
    return conn


def get_books():
    conn = open_connection()
    with conn.cursor() as cursor:
        result = cursor.execute('SELECT * FROM books;')
        books = cursor.fetchall()
        if result > 0:
            got_books = jsonify(books)
        else:
            got_books = 'No Books in DB'
        return got_books


def add_literature(book):
    conn = open_connection()
    with conn.cursor() as cursor:
        cursor.execute('INSERT INTO books (bookname, writer, literature, language, genre, description) VALUES(%s, %s, %s, %s, %s, %s)',
                       (book["bookname"], book["writer"], book["literature"], book["language"], book["genre"], book["description"]))
    conn.commit()
    conn.close()


