# -*- encoding: utf-8 -*-
##############################################################################
#
#    Brazilian Sale Order Taxes  module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Rafael da Silva Lima <rafael.lima@kmee.com.br>
#   
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
    'name' : 'Brazilian Sale Order Taxes',
    'description' : """
Module to handle taxes in sale order like IPI, ICMS""",
    'category' : 'Localization',
    'author' : 'KMEE',
    'maintainer': 'KMEE',
    'website' : 'http://www.kmee.com.br',
    'version' : '0.1',
    'depends' : [
                'l10n_br_sale_tax_in_price',
                'l10n_br_sale',
                'sale',
                ],
    'data': [
            'view/l10n_br_sale_tax_view.xml'
             ],
    'test': [],
    'installable': True,
    'images': [],
    'auto_install': False,
    'license': 'AGPL-3',
}