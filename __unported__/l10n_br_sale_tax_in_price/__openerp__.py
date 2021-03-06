# -*- encoding: utf-8 -*-
##############################################################################
#
#    Sale Tax in Price module for OpenERP
#    Copyright (C) 2014 KMEE (https://www.kmee.com.br).
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
{
    'name': 'Sale Tax add to sale price',
    'description': 'Add product tax in sale price on sale orders, use for add icms, pis, cofins to product final price',
    'category': 'sale',
    'license': 'AGPL-3',
    'author': 'KMEE',
    'website': 'www.kmee.com.br',
    'version': '7.0',
    'depends': ['sale'],
    'data': [
        'view/account_tax_view.xml',
        'view/sale_order_view.xml',
        ],
    'test': [],
    'demo': [],
    'installable': False,
    'active': False,
}
