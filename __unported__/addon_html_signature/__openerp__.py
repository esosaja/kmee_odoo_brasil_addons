# -*- encoding: utf-8 -*-
##############################################################################
#
#    KMEE Addon HTML Signature  module for OpenERP
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
    "name" : "Addon - HTML Signature",
    "version" : "1.0",
    "author" : "KMEE",
    "category": 'Kmee Addons',
    'complexity': "easy",
    "description": """
KMEE Addon - HTML Signature
====================================
This modules enables HTML signature in user preferences

for OpenERP 7.0

    """,
    'website': 'http://www.kmee.com.br',
    "depends" : [
        "email_template_attachment",
        "mail"
	],
    'init_xml': [],
    'update_xml': [
    	'view/res_users_view.xml',
    ],
    'demo_xml': [],
    'test': [],
    'application': False,
    'installable': False,
    'css': [
    ],
}

