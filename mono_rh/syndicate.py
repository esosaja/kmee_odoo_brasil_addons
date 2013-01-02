# coding: utf-8

import math

from osv import fields,osv
import tools
import pooler
from tools.translate import _

class res_partner_syndicate_ext(osv.osv):
	_inherit = 'res.partner'
	_columns = {
		'syndicate': fields.boolean('Sindicato', help="Check this box if the partner is a syndicate."),
	}
res_partner_syndicate_ext()


class hr_syndicate_br(osv.osv):
	_inherit = 'hr.employee'
	_columns = {
		'syndicate_rel': fields.many2many('hr.syndicate.br.reg', 'hr_syndicate_br_rel2', 'cpf', 'name', 'Sindicato'),
	}
hr_syndicate_br()


class hr_syndicate_br_reg(osv.osv):
	_name = 'hr.syndicate.br.reg'
	_columns = {
		'reference': fields.integer('Referencia'),
		'periodo': fields.date('Período'),
		'syndicate_opt': fields.many2one('res.partner', 'Sindicato', domain="[('syndicate','=',1)]"),
		'importancia': fields.float('Importância')
	}
hr_syndicate_br_reg()