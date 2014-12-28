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
#-
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

    def _prepare_order_line_invoice_line(self, cr, uid, line,
                                         account_id=False, context=None):

        result = super(SaleOrderLine, self)._prepare_order_line_invoice_line(
            cr, uid, line, account_id, context)

        result['price_unit'] = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
        result['discount'] = 0.00

        return result