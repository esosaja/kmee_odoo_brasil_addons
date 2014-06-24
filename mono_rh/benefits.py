#-*- encoding: utf-8 -*-

import time
import datetime
from osv import fields, osv
import tools
from tools.translate import _

class hr_benefits(osv.osv):
	_name = 'hr.benefits.br'
	_description = "Employee Benefits"
	_columns = {
		'benefit_id': fields.integer('Reference', size=3),
		'name': fields.char('Benefit', size=155, required=True),
		'value': fields.float('Value', required=True),
		#'benefits_tax': fields.one2many(''),
		
		
	}
hr_benefits()

class hr_employee_benefits(osv.osv):
	_inherit = 'hr.employee'
	_columns = {
		'benefit_ids': fields.many2many('hr.benefits.br', 'hr_employee_benefits2_rel', 'login', 'benefit_id', 'Benefits'),
	}
hr_employee_benefits()

class hr_benefits_benefits(osv.osv):
	_inherit = 'hr.benefits.br'
	_columns = {
		'tax_ids': fields.many2many('account.tax', 'hr_benefits_br_rel','benefit_id', 'tax_id', 'Default Taxes'),
	}
hr_benefits_benefits()

