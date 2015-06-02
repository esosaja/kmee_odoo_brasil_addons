# -*- encoding: utf-8 -*-
##############################################################################
#
#    Author: Luis Felipe Miléo - mileo @ kmee.com.br
#    Copyright 2014 KMEE - KM Enterprise Engineering
#    https://www.kmee.com.br
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

from openerp.osv import orm, fields

class AccountTaxCode(orm.Model):
    _inherit = 'account.tax.code'

    _columns = {
        'add_tax_on_sale_price': fields.boolean(
            'Add tax in sale price',
            help='Select this field for add this tax in sale price')
        }

class AccountTax(orm.Model):
    _inherit = 'account.tax'

    _columns = {
        'add_tax_on_sale_price': fields.boolean(
            'Add tax in sale price',
            help='Select this field for add this tax in sale price')
        }