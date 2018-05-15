#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 17:18:36
# @Author  : kaijiang liu (liukaijiang@outlook.com)
# @Link    : https://returnwow.github.io/
# @Version : $Id$

from aiohttp import web


async def index(request):
	return web.Response(body=b'<h1>Awesome</h1>', content_type="text/html")