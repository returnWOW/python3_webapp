#!/usr/bin/env python3
import logging
import os

class My_Logger(object):
	def __init__(self, file_name):
		self.file_path = 'log/%s' % file_name
		self.full_path = os.path.abspath(self.file_path)


	def init_file(self):
		with open(self.file_path, 'w+') as f:
			f.truncate()
			print('Init log file success')


	def get_logger(self):
		# size_log_file = 0
		if os.path.exists(self.full_path):
			size_log_file = self.get_FileSize()
			
			if size_log_file >= 5:
				print('Log file size is:%s' % size_log_file)
				self.init_file()

		logger = logging.getLogger('test')
		logger.setLevel(logging.INFO)
		log_file = logging.FileHandler(self.file_path)
		formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d %(levelname)s %(message)s')
		log_file.setFormatter(formatter)
		logger.addHandler(log_file)

		return logger


	def get_FileSize(self):
		# print()
		fsize = os.path.getsize(self.full_path)
		fsize = fsize/float(1024*1024)
		return round(fsize,2)