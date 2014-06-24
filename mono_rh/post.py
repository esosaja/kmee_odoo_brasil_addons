# -*- coding: utf-8 -*-

import time
from datetime import datetime
from osv import fields, osv
import tools
from tools.translate import _

""" Objeto Cargos """
class hrpost(osv.osv):
	_name = "hr.post.post"
	_description = "Human Resources Post"
	_columns = {
		'name': fields.char('Name', size=255, required=True, translate=True),
		'description': fields.text('Post Description', size=255, required=False),
		'category': fields.many2one('hr.post.category', 'Category'),
		'cbo': fields.many2one('hr.post.cbo', 'CBO Code'),
		'post_salary': fields.float('Post Salary', size=6, required=False),
	}
hrpost()

""" Objeto Categoria de Cargos """
class hrpost_category(osv.osv):
	_name = "hr.post.category"
	_description = "Human Resource Post Category"
	_columns = {
		'name': fields.char('Post Category', size=255, required=True, translate=True),
		'description': fields.text('Post Category Description', size=255, required=False),
	}
hrpost_category()

""" Objeto CBO """
class hr_cbo(osv.osv):
	_name = "hr.post.cbo"
	_description = "Brazilian Classification of Occupation"
	_columns = {
		'code': fields.integer('Code', size=4, required=True, translate=True),
		'name': fields.char('Name', size=255, required=True, translate=True),
	}
hr_cbo()