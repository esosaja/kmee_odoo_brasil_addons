# -*- coding: utf-8 -*-

import time
from datetime import datetime
from osv import fields, osv
import tools
from tools.translate import _

class hr_contract_ext(osv.osv):
	_inherit = 'hr.contract'
	_description = "Contract Extension BR"
	_columns = {
		'wage': fields.many2one('hr.contract.wage', 'Wage'),
	}

hr_contract_ext()

class hr_contract_wage(osv.osv):
	_name = 'hr.contract.wage'
	_description = "Wages for Contract"
	_columns = {
		'name': fields.float('Wage', digits=(16,2), required=True),
		'date_registry': fields.date('Date of Registry', select=True),
	}

hr_contract_wage()