# -*- encoding: utf-8 -*-
##############################################################################
#
#    KMEE Nfe Extended module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Matheus Lima Felix <matheus.felix@kmee.com.br>
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

from openerp.osv import fields, osv, orm
from openerp.tools.translate import _
from xml.dom import minidom
import base64
import shutil
from datetime import datetime
import time
import os

# Função de Export com problemas!
# Função _get_zip exporta o zip para pasta server do openerp, mais não filtra as datas, pois
# a função shutil.make_archive reúne todas pastas que tem dentro de homologação e passa para .zip
# Problema também no "directory" preciso especificar melhor o caminho (como efetuar o "monta_caminho")!

class validate_xml_to_zip(osv.osv_memory):
    _name = "validate_xml_to_zip"
    _description = "validate_xml_to_zip"
    
    def _get_zip(self, cr, uid, ids, fields, arg, context=None):
        res = {}
        directory = "/opt/data_openerp/eurocomponentes/exportacao/homologacao"
        for invoice in self.browse(cr, uid, ids):
            day_start = invoice.period_start_id
            day_start= time.strftime('%m')
            day_finish = invoice.period_finish_id
            day_finish = time.strftime('%m')
            date = os.listdir('/opt/data_openerp/eurocomponentes/exportacao/homologacao')
            date[0]  = time.strftime('%m')
            date[-1] = time.strftime('%m')
            if day_start >= date[0] and date[-1]<=day_finish:
                res[invoice.id] = shutil.make_archive("arquivo_zip", "zip", directory)
        return res
    
    def _export(self, cr, uid, ids, fields, arg, context=None):
         
        data = self.read(cr, uid, ids, [], context=context)[0]
        
        zipFile = self._get_zip(self, cr, uid, ids, data, fields, arg, context=None)      
        self.write(
                cr, uid, ids, {'zip_get': base64.b64encode(zipFile),
                'state': 'done', 'zip_name': 'zip_file.zip'}, fields, arg, context=context)
         
        mod_obj = self.pool.get('ir.model.data')
        model_data_ids = mod_obj.search(
            cr, uid, [('model', '=', 'ir.ui.view'),
            ('name', '=', 'validate_xml_to_zip_view')],
            context=context)
        resource_id = mod_obj.read(
            cr, uid, model_data_ids,
            fields=['res_id'], context=context)[0]['res_id']
 
        return {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': data['id'],
            'views': [(resource_id, 'form')],
            'target': 'new',
        }      
    _columns = {
        'Teste': fields.char('Teste'),
        'zip_name': fields.char('Name'),
        'period_start_id': fields.date('Período Inicial ', required=True, type="datetime"),
        'period_finish_id': fields.date('Periodo Final', required=True, type="datetime"),
        'state': fields.selection(
                [('init', 'init'), ('done', 'done')], 'state', readonly=True),
        'export': fields.function(_export),
        'zip_get': fields.function(_get_zip, type="binary", string="Download Arquivo Zip", method=True, store=False),
    }
      
    
    _defaults = {
                'state': 'init',
                }    
