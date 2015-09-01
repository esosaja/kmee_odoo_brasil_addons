# -*- coding: utf-8 -*-
#############################################################################
#
#    OpenERP, Open Source Management Solution
#    Authors: Michell Stuttgart <michell.stuttgart@kmee.com.br>
#    Copyright (C) 2015 KMEE <www.kmee.com.br>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of qhe
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


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    payment_term_id = fields.Many2one('account.payment.term',
                                      related='invoice.payment_term',
                                      string='Payment Terms', store=True)
