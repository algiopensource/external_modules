# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2011 Tiny SPRL (<http://tiny.be>).
#    Copyright (C) 2011 ChriCar Beteiligungs- und Beratungs- GmbH (<http://www.camptocamp.com>).
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
from openerp.osv import fields, osv
from openerp import fields as fields2


class stock_move (osv.osv):
    _inherit = "stock.move"
    def _create_invoice_line_from_vals(self, cr, uid, move, invoice_line_vals, context=None):
        invoice_line_vals['stock_move_id'] = move.id
        return super(stock_move, self)._create_invoice_line_from_vals(cr, uid, move, invoice_line_vals, context=context)


class stock_picking(osv.osv):
    _inherit = "stock.picking"

    _columns = {
        'invoice_ids': fields.many2many('account.invoice', 'picking_invoice_rel', 'picking_id', 'invoice_id', 'Invoices'),
        'client_order_ref' : fields.related ('sale_id', 'client_order_ref', type="char", relation="sale.order", string="Client Ref", readonly = True ),
    }
    purchase_id = fields2.Many2one(
        'purchase.order', related='move_lines.purchase_line_id.order_id',
        store=True)

    def init(self, cr):
        # This is a helper to guess "old" Relations between pickings and invoices
        cr.execute("""
insert into picking_invoice_rel(picking_id,invoice_id) select p.id,i.id from stock_picking p, account_invoice i
where p.name = split_part(i.origin,':',1) and (p.id,i.id) not in (select picking_id,invoice_id from picking_invoice_rel);
""")

    def action_invoice_create(self, cr, uid, ids, journal_id=False,
                              group=False, type='out_invoice', context=None):
        res = super(stock_picking, self).\
            action_invoice_create(cr, uid, ids, journal_id, group, type,
                                  context)
        invoice_ids = res
        inv_obj = self.pool.get('account.invoice')
        for inv in inv_obj.browse(cr, uid, invoice_ids):
            pick_ids = set()
            for l in inv.invoice_line:
                if l.stock_move_id and l.stock_move_id.picking_id:
                    pick_ids.add(l.stock_move_id.picking_id.id)
            pick_ids = list(pick_ids)
            inv.write({'picking_ids' : [(6,0, pick_ids )]})
        return res

    def copy(self, cr, uid, id, default=None, context=None):
        if default is None:
            default = {}
        default = default.copy()
        default.update({'invoice_ids': [],})
        return super(stock_picking, self).copy(cr, uid, id, default, context)
