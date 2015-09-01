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

    def _credit_debit_get_limit_2(self, cr, uid, ids, field_names, arg, context=None):

        result = {}
        for partner_id in ids:
            res = super(ResPartner, self)._credit_debit_get(cr, uid, ids, field_names, arg, context=context)
            result[partner_id] = {'credit_with_limit': res[partner_id]['credit'] if 'credit' in res[partner_id] else 0.00}
        return result

    def _credit_limit_search(self, cr, uid, obj, name, args, context=None):
        return self._asset_difference_credit_search(cr, uid, obj, name, 'receivable', args, context=context)

    def _asset_difference_credit_search(self, cr, uid, obj, name, type, args, context=None):

        if not args:
            return []
        having_values = tuple(map(itemgetter(2), args))
        where = ' AND '.join(
            map(lambda x: '(SUM(bal2) %(operator)s %%s)' % {'operator': x[1]}, args))

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
                            'AND (SELECT payment_mode_id FROM payment_mode_rel WHERE ' \
                                'payment_term_id=l.payment_term_id) IN (' \
                                'SELECT id FROM payment_mode WHERE ' \
                                'verify_credit_limit IS True)' \
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
        'credit_with_limit': fields.function(_credit_debit_get_limit_2, fnct_search=_credit_limit_search,
                                             string='Total recebivel com credito', type='float',
                                             multi='dc2', method=True, help="Total amount this customer owes you."),
    }

    # credit_with_limit = fields.Float(compute='_credit_debit_get_limit_2', search='_credit_limit_search',
    #                                  string='Total recebivel com credito')

