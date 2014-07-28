# # -*- encoding: utf-8 -*-
# ##############################################################################
# #
# #    KMEE Addon HTML Signature  module for OpenERP
# #    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
# #    @author Rafael da Silva Lima <rafael.lima@kmee.com.br>
# #   
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as
# #    published by the Free Software Foundation, either version 3 of the
# #    License, or (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
# from openerp.osv import orm, fields
# 
# 
# class CrmLead(orm.Model):
#     
#     _inherit = "crm.lead"
#     
#     def _get_default_email(self, cr, uid, context=None):
#         """ Gives partner email address for current lead
#         """
#         if context is None:
#             context = {}
#         obj_partner = self.pool.get("res.partner")
#         partner_id = obj_partner.search()
#     
#     _defaults = {  
#          'email_from': lambda self, cr, uid, c: self._get_default_email(cr, uid, c),
#     }