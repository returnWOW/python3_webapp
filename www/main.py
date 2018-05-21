#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 17:12:04
# @Author  : kaijiang liu (liukaijiang@outlook.com)
# @Link    : https://returnwow.github.io/
# @Version : $Id$


import os
import asyncio
from aiohttp import web
from routes import setup_routes
from log.log import My_Logger


SERVER_IP = '127.0.0.1'
SERVER_PORT = 8080


logger = My_Logger(os.path.splitext(__name__)[0] + '.log').get_logger()
def log(msg, file=''):
	logger.info('File:%s, Log:%s' % (file, msg)


async def init(loop):
	app = web.Application(loop=loop)
	setup_routes(app)
	srv = await loop.create_server(app.make_handler(), SERVER_IP, SERVER_PORT)
	log('Server started at http://%s:%s' % (SERVER_IP, SERVER_PORT))
	print('Server started at http://%s:%s' % (SERVER_IP, SERVER_PORT))
	return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()
# if __name__ == '__main__':
# 	print(__name__)
# else:
# 	print(__name__)
# 	print('import ok')