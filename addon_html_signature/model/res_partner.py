# -*- encoding: utf-8 -*-
##############################################################################
#
#    KMEE Addon HTML Signature  module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Rafael da Silva Lima <rafael.lima@kmee.com.br>
#   
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp.osv import osv

class ResPartner(osv.AbstractModel):
    #FIXIT: class contact_mixin_methods(osv.AbstractModel):
    #           _name = 'res.contact.mixin.methods'
    #  Não sobreescreve , verificar a herença de osv.AbstractModel
    # Arquivo addons/base/res/res_partner.py linha 171
    _inherit = "res.contact.mixin.methods"
    
    def onchange_contact_mixin(self, cr, uid, ids, contact_id, partner_id, context=None):
        res = super(ResPartner, self).onchange_contact_mixin(cr, uid, ids, contact_id, partner_id, context)
        print res
        return {'value': {'partner_id': contact_id}}