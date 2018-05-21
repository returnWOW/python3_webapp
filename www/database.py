#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2018-05-21 18:09:26
# @Author  : kaijiang liu (liukaijiang@outlook.com)
# @Link    : https://returnwow.github.io/
# @Version : $Id$

import aiomysql
from main import log

__pool = None

async def create_pool(loop, **kw):
	log('Create database connection pool......')
	global __pool
	__pool = await aiomysql.create_pool(
		    host=kw.get('host', 'localhost'),
		    port=kw.get('port', 3306),
		    user=kw['user'],
		    password=kw[password],
		    db=kw['db'],
		    charset=kw.get('charset', 'utf8'),
		    autocommit=kw.get('autocommit', True),
		    maxsize=kw.get('maxsize', 10),
		    minsize=kw.get('minsize', 1),
		    loop=loop
		)


async def select(sql, args, size=None):
	log(sql + ' args:' +','.join(args))
	global __pool
	with (await __pool) as conn:
		cur = await conn.cursor(aiomysql.DictCursor) # 词典游标？
		await cur.execute(sql.replace('?', '%s'), args or ())
		if size:
			rs = await cur.fetchmany(size)
		else:
			rs = await cur.fetchall()
		await cur.close() # with，不需要关闭conn（感觉连接池的工作也可以完成）
		log('row returned:%s' % len(rs))

		return rs

async def excute(sql, args):
	log(sql + ' args:' +','.join(args))
	global __pool
	with (await __pool) as conn:
		try:
			cur = conn.cursor()
			cur.excute(sql.replace('?', '%s'), args)
			affected = cur.rowcount
			await cur.close()
		except BaseException as e:
			raise

	return affected