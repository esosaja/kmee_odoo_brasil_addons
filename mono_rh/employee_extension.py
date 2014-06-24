# -*- coding: utf-8 -*-

import time
from datetime import datetime
from osv import fields, osv
import tools
from tools.translate import _


""" Objeto Extension """
class hr_employee_post(osv.osv):
	_inherit = 'hr.job'
	_description = "Post Job"
	_columns = {
		'post': fields.many2one('hr.post.post','Post'),
		
	}
hr_employee_post()

class hr_employee_post_job(osv.osv):
	_inherit = 'hr.employee'
	_description = "Post Job"
	_columns = {
		'post_employee': fields.many2one('hr.post.post', 'Post'),
		'job_id': fields.many2one('hr.job','Job', domain="[('post','=',post_employee)]"),
		
	}
hr_employee_post_job()

