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

from openerp import api, models, fields

class AccountProductFiscalClassification(models.Model):
    _inherit = 'account.fiscal.position'

    # message_id = fields.Many2many('invoice.message',
    #                               'invoice_message_fiscal_classification_rel',
    #                               'fiscal_classification_id',
    #                               'message_id',
    #                               string='Message')

    message_id = fields.Many2one(
        'invoice.message', u'Mensagem Fiscal',
        domain="[('message_type', '=', 'fiscal_position')]"
    )
