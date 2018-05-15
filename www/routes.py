#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-15 17:20:15
# @Author  : kaijiang liu (liukaijiang@outlook.com)
# @Link    : https://returnwow.github.io/
# @Version : $Id$

from views import index


def setup_routes(app):
	app.router.add_get('/', index)
