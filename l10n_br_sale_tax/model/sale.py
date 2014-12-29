# -*- encoding: utf-8 -*-
# #############################################################################
#
# Brazilian Sale Order Taxes  module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Luis Felipe Mileo <mileo@kmee.com.br>
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

from openerp.osv import fields, orm
from openerp.addons import decimal_precision as dp

class SaleOrderLine(orm.Model):

    def _amount_tax_icmsst(self, cr, uid, tax=None):
        return {
            'icms_st_value': tax.get('amount', 0.0),
        }

    def _amount_tax_icms(self, cr, uid, tax=None):
        return {
            'icms_value': tax.get('amount', 0.0),
        }

    def _amount_tax_ipi(self, cr, uid, tax=None):
         return {
             'ipi_value': tax.get('amount', 0.0),
         }

    def _get_taxes(self, cr, uid, taxes_calculed):
        """

        :param cr:
        :param uid:
        :param taxes_calculed:
        :return:
        """
        common_taxes = [tx for tx in taxes_calculed['taxes'] if tx['domain'] in ['icms','ipi','icmsst']]
        result = {

        }
        for tax in common_taxes:
            try:
                amount_tax = getattr(
                    self, '_amount_tax_%s' % tax.get('domain', ''))
                result.update(amount_tax(cr, uid, tax))
            except AttributeError:
                # Caso não exista campos especificos dos impostos
                # no documento fiscal, os mesmos são calculados.
                continue
        return result

    def _amount_line(self, cr, uid, ids, field_name, arg, context=None):
        tax_obj = self.pool.get('account.tax')
        cur_obj = self.pool.get('res.currency')
        res = {}

        if context is None:
            context = {}
        for line in self.browse(cr, uid, ids, context=context):
            res[line.id] = {
                'price_subtotal': 0.0,
                'price_gross': 0.0,
                'discount_value': 0.0,
                'icms_value': 0.0,
                'icms_st_value': 0.0,
                'ipi_value': 0.0,
                'price_liquid': 0.0,
                'price_total': 0.0,
            }
            price = line.price_unit * (1 - (line.discount or 0.0) / 100.0)
            taxes = tax_obj.compute_all(cr, uid, line.tax_id, price,
                line.product_uom_qty, line.order_id.partner_invoice_id.id,
                line.product_id, line.order_id.partner_id,
                fiscal_position=line.fiscal_position,
                insurance_value=line.insurance_value,
                freight_value=line.freight_value,
                other_costs_value=line.other_costs_value)
            cur = line.order_id.pricelist_id.currency_id
            res[line.id].update(self._get_taxes(cr, uid, taxes))
            res[line.id]['price_liquid'] = line.price_list * line.product_uom_qty
            res[line.id]['price_subtotal'] = cur_obj.round(cr, uid, cur, taxes['total'])
            res[line.id]['price_gross'] = line.price_unit * line.product_uom_qty
            res[line.id]['discount_value'] = res[line.id]['price_gross']-(price * line.product_uom_qty)
            res[line.id]['price_total'] = taxes['total_included'] - taxes['total_tax_discount']
        return res


    _inherit = "sale.order.line"

    _columns = {
        'icms_value': fields.function(
            _amount_line, string=u'Vlr. ICMS',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'icms_st_value': fields.function(
            _amount_line, string=u'Vlr. ICMS ST',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'ipi_value': fields.function(
            _amount_line, string=u'Vlr. IPI',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'price_liquid': fields.function(
            _amount_line, string=u'Vlr. Liquido',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'discount_value': fields.function(
             _amount_line, string=u'Vlr. Desc. (-)',
             digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'price_gross': fields.function(
            _amount_line, string=u'Vlr. Bruto',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'price_subtotal': fields.function(
            _amount_line, string=u'Subtotal',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
        'price_total': fields.function(
            _amount_line, string=u'Total',
            digits_compute=dp.get_precision('Sale Price'), multi='sums'),
    }

    _defaults = {
        'icms_value': 0.0,
        'ipi_value': 0.0,
    }

    def _validate_totals(self, cr, uid, values, context=None):
        """Verifica se o valor dos campos dos impostos estão sincronizados
        com os impostos do OpenERP"""
        if not context:
            context = {}

        tax_obj = self.pool.get('account.tax')

        if (not values.get('product_id')
                or not values.get('product_uom_qty')
                or not values.get('fiscal_position')):
            order_line_id = context.get('order_line_id', False)
            if not order_line_id:
                return {}
            elif isinstance(order_line_id, (list)) and not len(order_line_id) == 1:
                return {}
            else:
                if isinstance(order_line_id, (int)):
                    order_line_id = [order_line_id]
                old = self.read(cr, uid, order_line_id,[
                    'fiscal_position', 'product_id', 'price_unit',
                     'company_id', 'invoice_line_tax_id', 'partner_id',
                     'quantity'])[0]
                for aux in old:
                    if isinstance(old[aux], (tuple)):
                        old[aux] = old[aux][0]
                old['invoice_line_tax_id'] = [[6, 0, old['invoice_line_tax_id']]]
                values = dict(old.items() + values.items())

        result = {}

        taxes = tax_obj.browse(
            cr, uid, values.get('tax_id')[0][2])

        if values.get('partner_id') and values.get('shop_id'):
            partner_id = values.get('partner_id')
            shop_id = values.get('shop_id')
            pricelist_id = values.get('pricelist_id')
        else:
            if values.get('order_id'):
                order = self.pool.get('sale.order').read(
                    cr, uid, values.get('order_id'), ['partner_id', 'shop_id','pricelist_id'])
                partner_id = order.get('partner_id', [False])[0]
                shop_id = order.get('shop_id', [False])[0]
                pricelist_id = order.get('pricelist_id', [False])[0]

        obj_shop = self.pool.get('sale.shop').browse(cr, uid, shop_id)
        company_id = obj_shop.company_id.id

        obj_pricelist = self.pool.get('product.pricelist').browse(cr, uid, pricelist_id)

        fiscal_position = self.pool.get('account.fiscal.position').browse(
            cr, uid, values.get('fiscal_position'))

        price_unit = values.get('price_unit', 0.0)
        price_list = values.get('price_list', 0.0)
        product_uom_qty = values.get('product_uom_qty', 0.0)
        price = price_unit * (1 - values.get('discount', 0.0) / 100.0)
        tax_obj = self.pool.get('account.tax')
        taxes_calculed = tax_obj.compute_all(
            cr, uid, taxes, price, values.get('product_uom_qty', 0.0),
            values.get('product_id'), partner_id,
            fiscal_position=fiscal_position,
            insurance_value=values.get('insurance_value', 0.0),
            freight_value=values.get('freight_value', 0.0),
            other_costs_value=values.get('other_costs_value', 0.0))

        if context.get('operation', 'on_change') not in ('create', 'write'):
            cur_obj = self.pool.get('res.currency')
            cur = obj_pricelist.currency_id
            result['price_subtotal'] = cur_obj.round(cr, uid, cur, taxes_calculed['total_included'])
            result['price_gross'] = cur_obj.round(cr, uid, cur, taxes_calculed['total'])
            result['price_liquid'] = price_list * product_uom_qty
            result['discount_value'] = cur_obj.round(cr, uid, cur, result['price_gross'] - (price * product_uom_qty))
            result['price_total'] = taxes_calculed['total_included'] - taxes_calculed['total_tax_discount']
        result.update(self._get_taxes(cr, uid, taxes_calculed))
        return result

    def product_id_change(self, cr, uid, ids, pricelist, product, qty=0,
                          uom=False, qty_uos=0, uos=False, name='',
                          partner_id=False, lang=False, update_tax=True,
                          date_order=False, packaging=False,
                          fiscal_position=False, flag=False, context=None):
        if not context:
            context = {}

        result_super = super(SaleOrderLine, self).product_id_change(
            cr, uid, ids, pricelist, product, qty,
                          uom, qty_uos, uos, name,
                          partner_id, lang, update_tax,
                          date_order, packaging,
                          fiscal_position, flag, context)

        values = {
            'partner_id': partner_id,
            'product_id': product,
            'product_uom_qty': qty,
            'pricelist_id': pricelist,
            'shop_id' : context.get('shop_id', [False]),
            'price_unit': result_super['value'].get('price_unit'),
            'price_list': result_super['value'].get('price_list'),
            'fiscal_position': result_super['value'].get('fiscal_position'),
            'tax_id': [[6, 0, result_super['value'].get('tax_id')]],
        }

        result_super['value'].update(self._validate_totals(cr, uid, values, context))
        return result_super

    def create(self, cr, uid, vals, context=None):
        if not context:
            context = {}
        vals.update(self._validate_totals(cr, uid, vals, context))
        return super(SaleOrderLine, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        if not context:
            context = {}
        vals.update(self._validate_totals(cr, uid, vals, context))
        return super(SaleOrderLine, self).write(
            cr, uid, ids, vals, context=context)