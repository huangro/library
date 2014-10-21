#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb

class Database:
    def __init__(self, config):
	self.config = config
	self.conn = None
	self.cur = None
    
    def connect(self):
	self.conn = MySQLdb.connect(
	    host = self.config.get('host'), 
	    user = self.config.get('user'), 
	    passwd = self.config.get('pwd'), 
	    port = self.config.get('port'), 
	    charset = self.config.get('charset')
	)
	self.cur = self.conn.cursor()
	self.conn.select_db(self.config.get('name'))

    def close(self):
	if self.cur is not None:
	    self.cur.close()
	if self.conn is not None:
	    self.conn.close()

    def get(self, sql, one=True):
	"""
	Query database and get records
	"""
	if self.cur is not None:
	    self.cur.execute(sql)
	    if one:
		records = self.cur.fetchone()
	    else:
		records = self.cur.fetchall()
	else:
	    records = None
	return records

    def add(self, sql):
	"""
	Insert data into database
	"""
	if self.cur is not None:
	    self.cur.execute(sql)
	    result = True
	else:
	    result = False
	return result

    def delete(self, sql):
	"""
	Delete data from database
	"""
	if self.cur is not None:
	    self.cur.execute(sql)
	    result = True
	else:
	    result = False
	return result

    def update(self, sql):
	"""
	Update data to database
	"""
	if self.cur is not None:
	    self.cur.execute(sql)
	    result = True
	else:
	    result = False
	return result

