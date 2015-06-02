# -*- encoding: utf-8 -*-
##############################################################################
#
#    Brazillian Localization Base Calendar module for OpenERP
#    Copyright (C) 2014 KMEE (http://www.kmee.com.br)
#    @author Rafael da Silva Lima <rafael.lima@kmee.com.br>
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

from osv import fields,osv
from openerp import tools, SUPERUSER_ID
from datetime import datetime, timedelta, date

import pytz

html_invitation = """
<html>
<head>
<meta http-equiv="Content-type" content="text/html; charset=utf-8" />
<title>%(name)s</title>
</head>
<body>
<table border="0" cellspacing="10" cellpadding="0" width="100%%"
    style="font-family: Arial, Sans-serif; font-size: 14">
    <tr>
        <td width="100%%">Ol&aacute;,</td>
    </tr>
    <tr>
        <td width="100%%">Voc&ecirc; foi convidado para uma reuni&atilde;o da empresa <i>%(company)s</i>.</td>
    </tr>
    <tr>
        <td width="100%%">Abaixo est&atilde;o os detalhes do evento. Horas e datas expressas no fuso hor&aacute;rio  %(timezone)s .</td>
    </tr>
</table>

<table cellspacing="0" cellpadding="5" border="0" summary=""
    style="width: 90%%; font-family: Arial, Sans-serif; border: 1px Solid #ccc; background-color: #f6f6f6">
    <tr valign="center" align="center">
        <td bgcolor="DFDFDF">
        <h3>%(name)s</h3>
        </td>
    </tr>
    <tr>
        <td>
        <table cellpadding="8" cellspacing="0" border="0"
            style="font-size: 14" summary="Eventdetails" bgcolor="f6f6f6"
            width="90%%">
            <tr>
                <td width="21%%">
                <div><b>In&iacute;cio</b></div>
                </td>
                <td><b>:</b></td>
                <td>%(start_date)s</td>
                <td width="15%%">
                <div><b>Fim</b></div>
                </td>
                <td><b>:</b></td>
                <td width="25%%">%(end_date)s</td>
            </tr>
            <tr valign="top">
                <td><b>Descri&ccedil;&atilde;o</b></td>
                <td><b>:</b></td>
                <td colspan="3">%(description)s</td>
            </tr>
            <tr valign="top">
                <td>
                <div><b>Local</b></div>
                </td>
                <td><b>:</b></td>
                <td colspan="3">%(location)s</td>
            </tr>
            <tr valign="top">
                <td>
                <div><b>Participantes</b></div>
                </td>
                <td><b>:</b></td>
                <td colspan="3">
                <div>
                <div>%(attendees)s</div>
                </div>
                </td>
            </tr>
        </table>
        </td>
    </tr>
</table>
<table border="0" cellspacing="10" cellpadding="0" width="100%%"
    style="font-family: Arial, Sans-serif; font-size: 14">
    <tr>
        <td width="100%%">De:</td>
    </tr>
    <tr>
        <td width="100%%">%(user)s</td>
    </tr>
    <tr valign="top">
        <td width="100%%">-<font color="a7a7a7">-------------------------</font></td>
    </tr>
    <tr>
        <td width="100%%"> <font color="a7a7a7">%(sign)s</font></td>
    </tr>
</table>
</body>
</html>
"""



class BaseCalendar(osv.osv):
    
   _inherit = 'calendar.attendee'
   
   def _send_mail(self, cr, uid, ids, mail_to, email_from=tools.config.get('email_from', False), context=None):
        parent_res = super(BaseCalendar, self)._send_mail(cr, uid, ids, mail_to,  email_from=tools.config.get('email_from', False), context=context)
        
        
        company = self.pool.get('res.users').browse(cr, uid, uid, context=context).company_id.name
        for att in self.browse(cr, uid, ids, context=context):
            sign = att.sent_by_uid and att.sent_by_uid.signature or ''
            sign = '<br>'.join(sign and sign.split('\n') or [])
            res_obj = att.ref
            if res_obj:
                att_infos = []
                sub = res_obj.name
                other_invitation_ids = self.search(cr, uid, [('ref', '=', res_obj._name + ',' + str(res_obj.id))])

                for att2 in self.browse(cr, uid, other_invitation_ids):
                    att_infos.append(((att2.user_id and att2.user_id.name) or \
                                 (att2.partner_id and att2.partner_id.name) or \
                                    att2.email) + ' - Status: ' + att2.state.title())
                #dates and times are gonna be expressed in `tz` time (local timezone of the `uid`)
                tz = context.get('tz', pytz.timezone('UTC'))
                #res_obj.date and res_obj.date_deadline are in UTC in database so we use context_timestamp() to transform them in the `tz` timezone
                date_start = fields.datetime.context_timestamp(cr, uid, datetime.strptime(res_obj.date, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
                date_stop = False
                if res_obj.date_deadline:
                    date_stop = fields.datetime.context_timestamp(cr, uid, datetime.strptime(res_obj.date_deadline, tools.DEFAULT_SERVER_DATETIME_FORMAT), context=context)
                body_vals = {'name': res_obj.name,
                            'start_date': date_start,
                            'end_date': date_stop,
                            'timezone': tz,
                            'description': res_obj.description or '-',
                            'location': res_obj.location or '-',
                            'attendees': '<br>'.join(att_infos),
                            'user': res_obj.user_id and res_obj.user_id.name or 'OpenERP User',
                            'sign': sign,
                            'company': company
                }
                body = html_invitation % body_vals
                if mail_to and email_from:
                    ics_file = self.get_ics_file(cr, uid, res_obj, context=context)
                    vals = {'email_from': email_from,
                            'email_to': mail_to,
                            'state': 'outgoing',
                            'subject': sub,
                            'body_html': body,
                            'auto_delete': True}
                    if ics_file:
                        vals['attachment_ids'] = [(0,0,{'name': 'invitation.ics',
                                                        'datas_fname': 'invitation.ics',
                                                        'datas': str(ics_file).encode('base64')})]
                    self.pool.get('mail.mail').create(cr, uid, vals, context=context)
            return True
