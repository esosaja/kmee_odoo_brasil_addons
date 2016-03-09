# -*- coding: utf-8 -*-
##############################################################################
#
#   Copyright (c) 2016 Kmee - www.kmee.com.br
#   @author Luiz Felipe do Divino
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


class AccountInvoiceFiscalMessage(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def nfe_export(self):

        for inv in self:
            messages_invoice = []

            messages_invoice.append(
                inv.company_id.invoice_message.message_invoice
            )

            for invoice_line in inv.invoice_line:
                for fiscal_position in invoice_line.fiscal_position:
                    if fiscal_position.message_id:
                        messages_invoice.append(
                            fiscal_position.message_id.message_invoice
                        )
                for fiscal_category_id in invoice_line.fiscal_category_id:
                    if fiscal_category_id.message_id:
                        messages_invoice.append(
                            inv.fiscal_category_id.message_id.message_invoice
                        )

            if messages_invoice[0]:
                messages_list = []

                for message in messages_invoice:
                    if message not in messages_list:
                        messages_list.append(message)

                if inv.comment:
                    inv.comment += ' - ' + ' - '.join(messages_list)
                else:
                    inv.comment = ' - '.join(messages_list)

            super(AccountInvoiceFiscalMessage, self).nfe_export()
