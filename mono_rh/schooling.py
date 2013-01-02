# -*- coding: utf-8 -*-

import time
from datetime import datetime
from osv import fields, osv
import tools
from tools.translate import _

class hr_schooling_school(osv.osv):
    _name = 'hr.schooling.school'
    _description = 'School'
    _columns = {      
        'name': fields.char('School Name', size=255, required=True),
        'state_id': fields.many2one('res.country.state','State'),
        'city_id': fields.many2one('l10n_br_base.city','City', domain="[('state_id','=',state_id)]"),
        'description': fields.text('Description', size=255)
    }
hr_schooling_school()

class hr_schooling_course(osv.osv):
    _name = 'hr.schooling.course'
    _description = 'Schooling Course'
    _columns = {
        'name': fields.char('Course Name', size=255, required=True),
        'description': fields.text('Decription', size=255, required=False),
    }
   
    #_defaults = {
    #    'course_id': lambda obj, cr, uid, context: obj.pool.get('ir.sequence').get(cr, uid,'hr.schooling.course'),
    #}   
hr_schooling_course()

class hr_schooling_relation(osv.osv):
    _name = 'hr.schooling.relation'
    _description = 'Employee School'
    _order = 'course desc'
    _columns = {
        'course': fields.many2one('hr.schooling.course', 'Course'),
        'school': fields.many2one('hr.schooling.school', 'School'),
        'data_inicio': fields.date('Data de Início'),
        'data_fim': fields.date('Data do Término'),
        'duracao': fields.float('Duração'),
        
    }
hr_schooling_relation()

class hr_employee_schooling_option(osv.osv):
    _inherit = 'hr.employee'
    _columns = {
        'school_course': fields.many2many('hr.schooling.relation','hr_employee_school_course_rel','cpf','school', 'School and Course'),
        'anexos': fields.one2many('ir.attachment','res_id', 'Anexos'),
    }
hr_employee_schooling_option()

