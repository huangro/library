#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import sys
import time
import xlrd
import xlwt
import urllib
import urllib2
from datetime import datetime, timedelta
from HTMLParser import HTMLParser

def get_html_data(url):
    """
    Get html content data
    """
    res = urllib.urlopen(url)
    data = res.read()
    res.close()
    return data

def get_advance_html_data(header, url, timeout=5):
    """
    Get html content data by minitor browser's action
    """
    req = urllib2.Request(url, None, header)
    rsp = urllib2.urlopen(req, None, timeout)
    data = rsp.read()
    rsp.close()
    return data

def format_item(item):
    """
    format item to ignore sepcial characters
    """
    if item:
	value = item.replace("'", "\\'")
    else:
	value = ''
    return value

def encode_item(item):
    """
    Encode item to utf8
    """
    if item:
	value = item.replace("'", "\\'").strip()
    else:
	value = ''
    value = value.encode('utf8')
    return value

def read_excel(file_path):
    """
    Read excel data from file
    """
    if os.path.isfile(file_path):
	try:
	    data = xlrd.open_workbook(file_path)
	    return data
	except Exception, e:
	    print str(e)
	    return None
    else:
	return None
    
def get_excel_data_records(file_path, sheet_index=0, colname_index=0):
    """
    Get excel sorted data
    """
    data = read_excel(file_path)
    table = data.sheets()[sheet_index]
    nrows = table.nrows
    ncols = table.ncols
    col_names = table.row_values(colname_index)
    records = []
    for num in range(1, nrows):
	row = table.row_values(num)
	if row:
	    records.append(row)
    return records

def export_excel(data, file_path, columns, sheet_name='Default'):
    """
    Export excel file
    """
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "SimSum"
    style.font = font
    book = xlwt.Workbook(encoding='utf-8')
    book.set_height(3000)
    sheet1 = book.add_sheet(sheet_name)
    total = len(columns)
    for i in range(total):
	sheet1.col(i).width = columns[i][1]
    for i in range(total):
	sheet1.write(0, i, columns[i][0], xlwt.easyxf('font:height 300,colour_index brown; align:horz left, vert centre;'))
    count = 1
    for item in data:
	for i in range(total):
	    try:
		sheet1.write(count, i, item[i])
	    except:
		pass
	count += 1
    book.save(file_path)

def get_format_time(str_time):
    """
    Get format time
    """
    t_len = len(str_time)
    if t_len == 6:
	f_time = str_time[:2] + ':' + str_time[2:4] + ':' + str_time[4:]
    elif t_len == 5:
	f_time = '0' + str_time[0] + ':' + str_time[1:3] + ':' + str_time[3:]
    elif t_len == 4:
	f_time = '00:' + str_time[:2] + ':' + str_time[2:]
    elif t_len == 3:
	f_time = '00:0' + str_time[0] + ':' + str_time[1:]
    elif t_len == 2:
	f_time = '00:00:' + str_time
    elif t_len == 1:
	f_time = '00:00:0' + str_time
    else:
	f_time = '00:00:00'
    return f_time

def unescape_string(item):
    """
    Unescape string 
    """
    parser = HTMLParser()
    result = parser.unescape(item)
    return result

def datetime_to_seconds(date_time):
    """
    Format datetime %Y-%m-%d %H:%M:%S to seconds
    """
    my_format = '%Y-%m-%d %H:%M:%S'
    py_time = time.strptime(date_time, my_format)
    seconds = time.mktime(py_time)
    return int(seconds)

def datetime_min_datetime(d1, d2):
    """
    Caculate the minus of two string formated datetime 
    """
    d1 = datetime_to_seconds(d1)
    d2 = datetime_to_seconds(d2)
    return d2 - d1

def date_change(my_date, num):
    """
    Change date 
    """
    my_format = '%Y-%m-%d'
    d1 = datetime.strptime(my_date, my_format)
    d2 = d1 + timedelta(num)
    rs_date = datetime.strftime(d2, my_format)
    return rs_date
