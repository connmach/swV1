## PACKAGE IMPORTS



from functools import wraps
import  json, sqlite3
import logging
from flask import g, Flask, render_template, redirect, url_for, request
import MySQLdb
DATABASE = 'database.db' # database location

def connect():
    MYSQL_HOST= 'socialwings.mysql.pythonanywhere-services.com'
    MYSQL_USER= 'socialwings'
    MYSQL_PASSWORD='Test@1234'
    MYSQL_DB='socialwings$sw_ilp'

    conn=MySQLdb.connect (MYSQL_HOST,MYSQL_USER,MYSQL_PASSWORD,MYSQL_DB)

    return conn;

#make a db connection
def get_db():

    return connect()

#close connection on app teardown


#query the database
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

#insert a value into the db
def insert_db(query, args=()):
	""" USED LIKE SO:
			insert_db('insert into entries (title, text) values (?, ?)',[request.form['title'], request.form['text']])
	"""
	db = get_db()
	db.execute(query, args)
	db.commit()


