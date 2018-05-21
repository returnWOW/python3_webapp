#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import re
import csv
import time
import socket
import codecs
import aiohttp, asyncio
from log.log import My_Logger
# from max_index import get_url_max_index
# from tools.tool_http_data import ungzip, deflate

RAW_URL_FILE = '.\\result\\dns_url_2.txt' #URL源数据
RESULT_FOLDER = 'result'  #结果保存文件夹
RESULT_FILE = 'result_url_cate_other_localpc.txt'  #保存结果的文件
RESULT_URL_HISTORY = 'result/history'  #访问URL历史记录，包含重定向等URL
RESULT_HISTORY_FILE = 'urls_urls_cate_other_localpc.txt'
time_start = time.time()

url_lists = []
url_url_lists = {}

logger = My_Logger('pure_coroutie.py.log').get_logger()
log = lambda msg: logger.info(msg)


pattern_refresh = re.compile(b'http-equiv=(.*?)refresh(.*?)url=(.*?)["\']', re.IGNORECASE)

headers = {
	'Connection': 'Keep-alive',
	'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Accept-Language': 'zh-CN,zh;q=0.8',
	'Upgrade-Insecure-Requests': '1'
}


def read_handled_url():
	al_handle_url = [] #将已经处理完毕的URL获取出来，做过滤，后期可以完成对出错的URL再次进行处理。
	result_file = os.path.join(RESULT_FOLDER, RESULT_FILE)

	if os.path.exists(result_file):
		with codecs.open(result_file, 'r', 'utf-8') as fin:
			for line in fin:
				if 'index' not in line or line != '\n':
					index, raw_url, url = line.split('|')
					al_handle_url.append(raw_url)
	return al_handle_url

def read_raw_url():
	if os.path.splitext(RAW_URL_FILE)[-1] == '.csv':
		csv_reader = csv.reader(open(RAW_URL_FILE, encoding='utf-8'))
		return [url for url in csv_reader]
	elif os.path.splitext(RAW_URL_FILE)[-1] == '.txt':
		with codecs.open(RAW_URL_FILE, 'r', 'utf-8') as fin:
			return [url.split('\n')[0].split('|')[-1] for url in fin.readlines()]
	return None


def init():
	pass

def my_print(elemts):
	if isinstance(elemts, dict):
		for k, v in elemts.items():
			print(k, v)
	elif isinstance(elemts, (list, tuple, set)):
		for v in elemts:
			print(v)
	else:
		print(elemts)

def save_html(url, html):
	with codecs.open('result/local_html/%s.html' % url, 'w', 'utf-8') as fout:
		fout.write(html)
		print('save html:%s' % url)

count = 0
async def fetch(index, url, sem, len_url):
	# global log
	global url_lists, url_url_lists
	urls = []
	# log('Handle index:%s url:%s' % (index, url))
	# print('Total:%s handle:%s' % (len_url, count))
	try:
		async with sem:
				# count += 1
			async with aiohttp.ClientSession() as session:
				async with session.get(url, headers=headers, verify_ssl=False) as resp:
					if index % 1000 == 0:
						print('index:%s url:%s status:%s' % (index, url, resp.status))
					url = url.split('//')[-1]
					if resp.status in [200, 301, 302]:
						# print(index, url, resp.url.host)
						bin_html = await resp.read()
						# log('ok' + url)
						result = pattern_refresh.search(bin_html, re.S)
						# print(result)
						if result:
							link = result.group(3).decode()
							url2 = link if 'http' in link else '%s%s' % (url, link)
							# print(url2)
							async with session.get(url2,headers=headers) as resp:
								await resp.read()
						
						# save_html(url, bin_html.decode('utf-8'))

						# fout.write('%s|%s|%s\n' % (index, url, resp.url.host))
						# for history in resp.history:
						# 	urls.append(history.url.host)
						
						# if urls:
						# 	# url_url_lists[url] = urls
						# 	f_urls.write('%s|%s\n' % (url, ';'.join(urls)))
					else:
						log('index:%s url:%s status:%s' % (index, url, resp.status))
						# url_lists.append([index, url, resp.status])
						# fout.write('%s|%s|%s\n' % (index, url, resp.status))
						# log('index:%s url:%s code:%s' % (index, url, status))
	#这种错误，为了防止协程事件循环崩溃
	except Exception as e:
		log('Exception:%s Index:%s URL:%s' % (e, index, url))
		# url_lists.append([index, url, 'ERROR_%s' % e])
		# fout.write('%s|%s|%s\n' % (index, url.split('//')[-1], 'ERROR_%s' % e))
		# with open('error/pure_coroutine_error.txt', 'a') as f:
		# 	f.write('%s' % e)
		raise
		
async def bound_fetch(index, url, sem, len_url):
	async with sem:
		await fetch(index, url, sem, len_url)

async def run(loop, raw_urls):
	global log

	tasks = []
	sem = asyncio.Semaphore(500)
	len_url = len(raw_urls)
	print('Handle URL Counts:%s' % len_url)
	print('Save file %s' % os.path.join(RESULT_FOLDER, RESULT_FILE))
	print('history file: %s/%s' % (RESULT_URL_HISTORY, RESULT_HISTORY_FILE))
	log('%s%s%s' % ('*'*25, 'Start url count:%s' % len_url, '*'*25))
	index = 0
	# with codecs.open('%s' % os.path.join(RESULT_FOLDER, RESULT_FILE), 'a', 'utf-8') as fout:
		# with codecs.open('%s/%s' % (RESULT_URL_HISTORY, RESULT_HISTORY_FILE), 'a', 'utf-8') as f_urls:
			# if not max_index:
			# 	fout.write('%s|%s|%s\n' % ('index', 'raw_url', 'url'))
	if len(raw_urls[0]) == 2:
		for index, url in raw_urls:
			url = 'http://' + url
			task = asyncio.ensure_future(bound_fetch(index, url, sem, len_url))
			tasks.append(task)
	elif len([raw_urls[0]]) == 1:
		for url in raw_urls:
			url = 'http://' + url
			index += 1  #
			task = asyncio.ensure_future(bound_fetch(index, url, sem, len_url))
	

			resp = await asyncio.gather(task)
				# return resp
# async def run_html(loop, raw_urls, max_index):
	

def save(max_index):
	my_print(url_lists)
	my_print(url_url_lists)
	if url_lists:
		with codecs.open('%s' % os.path.join(RESULT_FOLDER, RESULT_FILE), 'a', 'utf-8') as fout:
			if not al_handled_url:
				fout.write('%s|%s|%s\n' % ('index', 'raw_url', 'url'))
			for index, raw_url, url in url_lists:
				fout.write('%s|%s|%s\n' %(index, raw_url.split('//')[-1], url))
	if url_url_lists:
		for url, urls in url_url_lists.items():
			url = url.split('//')[-1]
			with codecs.open('result/urls/%s.txt' % url, 'w', 'utf-8') as fout:
				for u in urls:
					fout.write(u + '\n')
#执行入口 
def main():
	s = time.time()
	# with open(RAW_URL_FILE, 'r') as fin:
	# 	urls = [url.strip('\n') for url in fin.readlines()]
	urls = ['localhost:8080/']*10000
	loop = asyncio.get_event_loop()
	# init()
	future = asyncio.ensure_future(run(loop, urls))
	loop.run_until_complete(future)
	# al_handled_url = read_handled_url()
	# print('Total time:%.2f' % (time_end - time_start))
	print(time.time()-s)
	log('%s%s%s' % ('*'*25, 'END', '*'*25))

if __name__ == '__main__':
	main()