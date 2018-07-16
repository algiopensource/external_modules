# -*- coding: utf-8 -*-
# © 2016 Comunitea - Javier Colmenero <javier@comunitea.com>
# License AGPL-3 - See http://www.gnu.org/licenses/agpl-3.0.html
from odoo import models, fields, api, exceptions, _
import logging

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.queue_job.job import job
except ImportError:
    _logger.debug('Can not `import queue_job`.')
    import functools

    def empty_decorator_factory(*argv, **kwargs):
        return functools.partial
    job = empty_decorator_factory

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[('progress',
                                             'Confirm in Progress')])
    order_jobs_ids = fields.Many2many(comodel_name='queue.job',
                                      column1='order_id', column2='job_id',
                                      string="Queue orders", copy=False)
    last_job_failed = fields.Boolean('Last confirmation failed')

    @job
    @api.multi
    def batch_confirm_one_order(self):
        self.ensure_one()
        ctx = self._context.copy()
        ctx.update({'do_super': True})
        self.with_context(ctx).action_confirm()
        last_job = self.order_jobs_ids[-1]
        if last_job.state == 'failed':
            self.last_job_failed = True
            self.state = "pending"
        #self.env['res.users'].browse(notif_user).\
        #    notify_info('The confirmation batch order has finished')


    @api.multi
    def action_confirm(self):
        res = False
        icp = self.env['ir.config_parameter']
        queue_obj = self.env['queue.job']
        max_lines_len = int(icp.get_param('max_lines_confirm', '15'))
        for order in self:
            if not self._context.get('do_super', False) and \
                    len(order.order_line) >= max_lines_len:
                order.state = "progress"
                ctx = order._context.copy()
                ctx.update(company_id=order.company_id.id)
                notif_user = self.env.user.id
                order2 = self.with_context(ctx,tracking_disable=True).browse(order.id)
                res = order2.sudo().with_delay().batch_confirm_one_order()
                # Add job to the orders queue
                queue_ids = queue_obj.search([('uuid', '=', res.uuid)],
                                             limit=1)
                order2.sudo().order_jobs_ids |= queue_ids
                return True
            else:
                ctx = self._context.copy()
                ctx.update(tracking_disable=True)
                res = super(SaleOrder, self.with_context(ctx)).action_confirm()
        return res

    @api.multi
    def _cancel_order_jobs(self):
        for queue in self.mapped('order_jobs_ids'):
            if queue.state == 'started':
                return False
            elif queue.state in ('pending', 'enqueued', 'failed'):
                queue.sudo().unlink()
        return True

    @api.multi
    def action_cancel(self):
        for queue in self.mapped('order_jobs_ids'):
            if not self._cancel_order_jobs():
                raise exceptions.\
                    Warning(_('You can not cancel this order because'
                              ' there is a job running!'))
        res = super(SaleOrder, self).action_cancel()
        return res
