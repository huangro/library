#!/usr/bin/python
# -*- coding:utf-8 -*-
#----------------------------------------------------------------------------
# FTP process class
# @Author	robinhuang
# @Version	1.0
# @Date     2014-09-12
#----------------------------------------------------------------------------

from ftplib import FTP
import os
import sys
import time
import datetime
import socket

TIMEOUT = 300
DELETE_SOURCE = False

class MYFTP:
	def __init__(self, host_addr, username, password, remote_addr, port=21):
		self.host_addr = host_addr
		self.username = username
		self.password = password
		self.remote_addr = remote_addr
		self.port = port
		self.ftp = FTP()
		self.file_list = []

	def __del__(self):
		self.ftp.close()

	def login(self):
		"""
		Login to ftp
		"""
		ftp = self.ftp
		try:
			socket.setdefaulttimeout(TIMEOUT)
			ftp.set_pasv(1)
			curr_time = time.strftime('%Y-%m-%d %H:%M:%S')
			print '>>> Current time is: %s' % curr_time
			print '>>> Start to connect to %s' % self.host_addr
			ftp.connect(self.host_addr, self.port)
			print '>>> Connecting success, start to login...'
			ftp.login(self.username, self.password)
			print '>>> Login to %s now' % self.host_addr
		except:
			print '>>> Connect to %s failed' % self.host_addr

		try:
			ftp.cwd(self.remote_addr)
		except:
			print '>>> Access to dir: %s failed' % self.remote_addr

	def get_remote_file_size(self, remote_file):
		"""
		Get remote file size 
		"""
		try:
			remote_file_size = self.ftp.size(remote_file)
		except:
			remote_file_size = -1
		return remote_file_size

	def get_local_file_size(self, local_file):
		"""
		Get local file size 
		"""
		try:
			local_file_size = os.path.getsize(local_file)
		except:
			local_file_size = -2
		return local_file_size

	def is_same_size(self, remote_file, local_file):
		"""
		Match if remote file size is the same as local file size 
		"""
		remote_file_size = self.get_remote_file_size(remote_file)
		local_file_size = self.get_local_file_size(local_file)
		if remote_file_size == local_file_size:
			return True
		else:
			return False

	def get_filename(self, line):
		"""
		Get remote file name
		"""
		lst = line.strip().split(' ')
		val = []
		count = 0
		for item in lst:
			if item.strip():
				val.append(item.strip())
				if len(val) == 4:
					break
			count += 1
		name = ' '.join(lst[count:])
		if val[2] == '<DIR>':
			tag = 'd'
		else:
			tag = '-'
		file_arr = [tag, name]
		return file_arr

	def get_file_list(self, line):
		"""
		Get remote file list 
		"""
		ret_arr = []
		file_arr = self.get_fileame(line)
		if file_arr[1] not in ['.', '..']:
			self.file_list.append(file_arr)

	def download_file(self, remote_file, local_file):
		"""
		Download the remote file
		"""
		if self.is_same_size(remote_file, local_file):
			return 
		else:
			print '>>> Download %s ...' % local_file
			file_handler = open(local_file, 'wb')
			self.ftp.retrbinary('RETR %s' % (remote_file), file_handler.write)
			file_handler.close()

	def download_files(self, remote_dir, local_dir):
		"""
		Download files from the remote dir
		"""
		try:
			if remote_dir:
				self.ftp.cwd(remote_dir)
		except:
			return
		if not os.path.isdir(local_dir):
			os.makedirs(local_dir)
		self.file_list = []
		self.ftp.dir(self.get_file_list)
		remote_names = self.file_list
		for item in remote_names:
			file_type = item[0]
			file_name = item[1]
			encoded_name = file_name.encode('utf8')
			local = os.path.join(local_dir, encoded_name)
			if file_type == 'd':
				self.download_files(file_name, local)
				if DELETE_SOURCE:
					self.ftp.rmd(file_name)
			elif file_type == '-':
				dself.download_file(file_name, local)
				if DELETE_SOURCE:
					self.ftp.delete(file_name)
		self.ftp.cwd('..')

	
