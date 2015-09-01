# -*- coding: utf-8 -*-
#############################################################################
#
#    OpenERP, Open Source Management Solution
#    Authors: Luis Felipe Mileo <mileo@kmee.com.br>
#    Copyright (C) 2015 KMEE <www.kmee.com.br>
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
###############################################################################
from openerp import models, fields, api
from openerp.exceptions import Warning


class PaymentModel(models.Model):
    _inherit = 'payment.mode'

    verify_credit_limit = fields.Boolean(string='Verificar credito',  default=True)


class AccountPaymentTerm(models.Model):
    _inherit = 'account.payment.term'

    payment_mode_id = fields.Many2many('payment.mode', 'payment_mode_rel',
                                       'payment_term_id', 'payment_mode_id',
                                       string='Modo de pagamento')

    valor_minimo = fields.Float(string='Valor minimo de compra', default=0)
    valor_maximo = fields.Float(string='Valor maximo de compra', default=0)
    valor_fixo = fields.Float(string='Valor fixo', default=0)


class SaleOrder(models.Model):

    _inherit = 'sale.order'

    payment_term = fields.Many2one('account.payment.term', 'Payment Term',
                                   domain="[('payment_mode_id','=',payment_mode_id)]")

    @api.multi
    def test_exceptions(self):
        """
        Condition method for the workflow from draft to confirm
        """
        #
        # if not self.payment_mode_id.verificar_limite_credito:
        #     if self.amount_total < self.payment_term.valor_minimo:
        #         raise Warning('Valor de compra menor do que o valor minimo para essa operacao!')
        #         return False
        #
        #     if (self.amount_total > self.payment_term.valor_maximo) and self.payment_term.valor_maximo != 0:
        #         raise Warning('Valor de compra maior do que o valor maximo para essa operacao!')
        #         return False
        #     return True
        # else:
        #     if self.amount_total <= (self.partner_id.credit_limit - self.partner_id.credit):
        #
        #         if self.amount_total < self.payment_term.valor_minimo:
        #             raise Warning('Valor de compra menor do que o valor minimo para essa operacao!')
        #             return False
        #
        #         if(self.amount_total > self.payment_term.valor_maximo) or self.payment_term.valor_maximo != 0:
        #             raise Warning('Valor de compra maior do que o valor maximo para essa operacao!')
        #             return False
        #         return True
        #     raise Warning('Caloteeeeeeee! Credito disponivel: {}'.format(
        #         (self.partner_id.credit_limit - self.partner_id.credit)))
        #     return False

        return super(SaleOrder, self).test_exceptions()
