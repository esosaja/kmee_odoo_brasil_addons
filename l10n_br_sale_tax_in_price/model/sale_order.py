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
import openerp.addons.decimal_precision as dp

class SaleOrderLine(orm.Model):
    _inherit = 'sale.order.line'

    _columns = {
        'price_list': fields.float('List Price', required=True, digits_compute= dp.get_precision('Product Price'), readonly=True, states={'draft': [('readonly', False)]}),
    }

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='',
                          partner_id=False, lang=False, update_tax=True,
                          date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):
        #Force update tax
        update_tax = True

        result = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty, uom, qty_uos, uos, name,
            partner_id, lang, update_tax, date_order, packaging,
            fiscal_position, flag, context)

        result['value']['price_list'] = result['value']['price_unit']

        if result['value'].has_key('tax_id'):
            account_tax_obj = self.pool.get('account.tax')
            amount = 0
            for tax in account_tax_obj.browse(cr, uid, result['value']['tax_id']):
                if tax.add_tax_on_sale_price:
                    amount += tax.amount
            result['value']['price_unit'] = result['value']['price_unit'] / (1 - amount)
        return result