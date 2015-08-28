# -*- coding: utf-8 -*-
#############################################################################
#
#    OpenERP, Open Source Management Solution
#    Authors: Michell Stuttgart <michell.stuttgart@kmee.com.br>
#    Copyright (C) 2015 KMEE <www.kmee.com.br>
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

from openerp.osv import orm, fields
from operator import itemgetter


class ResPartner(orm.Model):

    _inherit = 'res.partner'

    def _credit_debit_get(self, cr, uid, ids, field_names, arg, context=None):
        ctx = context.copy()
        ctx['all_fiscalyear'] = True

        query = self.pool.get('account.move.line')._query_get(cr, uid, context=ctx)

        cr.execute("""SELECT l.partner_id, a.type, SUM(l.debit-l.credit)
                      FROM account_move_line l
                      LEFT JOIN account_account a ON (l.account_id=a.id)
                      WHERE a.type IN ('receivable','payable')
                      AND l.partner_id IN %s
                      AND l.reconcile_id IS NULL
                      AND """ + query + """
                      GROUP BY l.partner_id, a.type
                      """,
                   (tuple(ids),))
        maps = {'receivable': 'credit', 'payable': 'debit' }
        res = {}
        for id in ids:
            res[id] = {}.fromkeys(field_names, 0)
        for pid, type, val in cr.fetchall():
            if val is None:
                val = 0
            res[pid][maps[type]] = (type == 'receivable') and val or -val
        return res

    def _credit_limit_search(self, cr, uid, obj, name, args, context=None):
        return self._asset_difference_credit_search(cr, uid, obj, name, 'receivable', args, context=context)

    # def _debit_search(self, cr, uid, obj, name, args, context=None):
    #     return self._asset_difference_search(cr, uid, obj, name, 'payable', args, context=context)

    def _asset_difference_credit_search(self, cr, uid, obj, name, type, args, context=None):

        print 'respartner!!!!!'

        if not args:
            return []
        having_values = tuple(map(itemgetter(2), args))
        where = ' AND '.join(
            map(lambda x: '(SUM(bal2) %(operator)s %%s)' % {
                                'operator':x[1]},args))
        query = self.pool.get('account.move.line')._query_get(cr, uid, context=context)

        cr.execute(('SELECT pid AS partner_id, SUM(bal2) FROM ' \
                        '(SELECT CASE WHEN bal IS NOT NULL THEN bal ' \
                         'ELSE 0.0 END AS bal2, p.id as pid FROM ' \
                            '(SELECT (debit-credit) AS bal, partner_id ' \
                            'FROM account_move_line l ' \
                            'WHERE account_id IN ' \
                                '(SELECT id FROM account_account '\
                                'WHERE type=%s AND active) ' \
                            'AND reconcile_id IS NULL ' \
                            'AND payment_term_id.payment_mode_id in ('
                                'SELECT id from payment_mode where '
                                'verify_credit_limit is True )'
                            'AND '+query+') AS l ' \
                        'RIGHT JOIN res_partner p ' \
                        'ON p.id = partner_id ) AS pl ' \
                    'GROUP BY pid HAVING ' + where),
                    (type,) + having_values)
        res = cr.fetchall()
        if not res:
            return [('id', '=', '0')]
        return [('id', 'in', map(itemgetter(0), res))]

    _columns = {
        'credit': fields.function(_credit_debit_get, fnct_search=_credit_limit_search, string='Total Receivable',
                                  multi='dc', help="Total amount this customer owes you."),
    }


