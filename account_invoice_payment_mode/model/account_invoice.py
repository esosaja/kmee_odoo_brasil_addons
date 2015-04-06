# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
# Copyright (C) 2015  KMEE  - www.kmee.com.br - Bertozo                       #
#                                                                             #
# This program is free software: you can redistribute it and/or modify        #
# it under the terms of the GNU Affero General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or           #
# (at your option) any later version.                                         #
#                                                                             #
# This program is distributed in the hope that it will be useful,             #
# but WITHOUT ANY WARRANTY; without even the implied warranty of              #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the               #
# GNU General Public License for more details.                                #
#                                                                             #
# You should have received a copy of the GNU General Public License           #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.       #
###############################################################################

from openerp.osv import orm, fields


class AccountPaymentTerm(orm.Model):
    _inherit = "account.payment.term"

    def compute(self, cr, uid, id, value, date_ref=False, context=None):
        result = []
        list_ids = []
        if context is None:
            context = {}

        if 'acc_inv_payment_mode_ids' in context:
            for i in context['acc_inv_payment_mode_ids']:
                list_ids.append(i.id)

            acc_inv_payment_mode_obj = self.pool.get(
                'account.invoice.payment.mode').browse(cr, uid, list_ids)
            for i in acc_inv_payment_mode_obj:
                result.append((i.date_maturity, i.installment_amount))

        else:
            result = super(AccountPaymentTerm, self).compute(
                cr, uid, id, value, date_ref, context)

        return result


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    _columns = {
        'acc_inv_payment_mode_ids': fields.one2many(
            'account.invoice.payment.mode', 'acc_inv_payment_mode_id',
            'Maturity')
    }

    def onchange_payment_term_date_invoice(self, cr, uid, ids, payment_term_id,
                                           date_invoice):
        aux = []
        totlines = ()
        if not isinstance(ids, list):
            ids = [ids]

        if not ids:
            raise orm.except_orm((u'Atualize o total da fatura ou salve a '
                                  u'cotação'), "")

        for inv in self.browse(cr, uid, ids):
            res = super(AccountInvoice,
                        self).onchange_payment_term_date_invoice(
                cr, uid, ids, payment_term_id, date_invoice)
            if not date_invoice:
                date_invoice = fields.date.context_today(self, cr, uid)

            payment_term_obj = self.pool.get('account.payment.term')
            payment_mode_line_obj = \
                self.pool.get('account.invoice.payment.mode')
            total = inv.amount_total

            if inv.payment_term.id != payment_term_id:
                self.write(cr, uid, ids, {'payment_term': payment_term_id})
                totlines = payment_term_obj.compute(
                    cr, uid, payment_term_id, 1, date_invoice)
                list_ids = []
                if inv.acc_inv_payment_mode_ids:
                    for i in inv.acc_inv_payment_mode_ids:
                        list_ids.append(i.id)

                    payment_mode_line_obj.unlink(cr, uid, list_ids,
                                                 context=None)
                for i in totlines:
                    aux.append((0, 0, {'date_maturity': i[0],
                                       # 'percentage': i[1],
                                       'installment_amount': i[1] * total,
                                       'total': total}))

            res['value']['acc_inv_payment_mode_ids'] = aux

        return res

    def action_move_create(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        for inv in self.browse(cr, uid, ids, context=context):
            context['acc_inv_payment_mode_ids'] \
                = inv.acc_inv_payment_mode_ids
            result = super(AccountInvoice, self).action_move_create(
                cr, uid, ids, context)

        return True


class AccountInvoicePaymentMode(orm.Model):
    _name = 'account.invoice.payment.mode'

    _columns = {
        'acc_inv_payment_mode_id': fields.many2one('account.invoice', 'Ref'),
        'date_maturity': fields.date('Date Maturity'),
        'installment_amount': fields.float('Installment Amount')
    }
