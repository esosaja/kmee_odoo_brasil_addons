# -*- coding: utf-8 -*-
##############################################################################
#
#    KMEE, KM Enterprising Engineering
#    Copyright(C) 2014 - Fernando Marcato Rodrigues (<http://www.kmee.com.br>)
#
#    This program is free software: you can redistribute it and    /or modify
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
{
    'name': u'Sale Order fields position adjust',
    'version': '1.0',
    'category': 'Other',
    'description': u"""Módulo para ajustar as posições dos campos
    payment_mode_id, fiscal_category_id e fiscal_position para a aba "Itens
    do Pedido" da view Pedidos de Vendas""",
    'author': 'KMEE',
    'website': 'http://www.kmee.com.br',
    'depends': [
        'l10n_br_sale_stock',
        'account_payment_sale',
        'sale_journal',
    ],
    'data': [
        'view/sale_order_altered_view.xml'
    ],
    'installable': False,
    'auto_install': False,
}
