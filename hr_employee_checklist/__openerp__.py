# -*- encoding: utf-8 -*-
##############################################################################
#
#    Brazillian Human Resources Employee module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Rafael da Silva Lima <mileo@kmee.com.br>
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
    'name' : 'HR Employee Checklist',
    'description' : """
Checklist de documentos dos funcionários""",
    'category' : 'Localization',
    'author' : 'KMEE',
    'maintainer': 'KMEE',
    'website' : 'http://www.kmee.com.br',
    'version' : '0.1',
    'depends' : ['hr','l10n_br','l10n_br_base'],
    'init_xml': [],
    'data': [
             'view/hr_employee_view.xml',
             ],
    'update_xml' : [
    ],
    'test': [],
    'installable': True,
    'images': [],
    'auto_install': False,
    'license': 'AGPL-3',
}
