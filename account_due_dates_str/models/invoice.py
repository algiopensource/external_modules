# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Comunitea Servicios Tecnológicos All Rights Reserved
#    $Omar Castiñeira Saaevdra <omar@comunitea.com>$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
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

from odoo import models, fields, api, tools
import time
from datetime import datetime
from time import mktime


class AccountInvoice(models.Model):

    _inherit = "account.invoice"

    @api.one
    def _get_move_lines_str(self):
        """returns all move lines related to invoice in string"""
        expiration_dates_str = ""
        move_line_obj = self.env["account.move.line"]
        if self.move_id:
            move_lines = move_line_obj.\
                search([('move_id', '=', self.move_id.id),
                        ('account_id.internal_type', 'in',
                         ['payable', 'receivable']),
                        ('date_maturity', "!=", False)],
                       order="date_maturity asc")
            for line in move_lines:
                date = time.strptime(line.date_maturity, "%Y-%m-%d")
                date = datetime.fromtimestamp(mktime(date))
                date = date.strftime("%d/%m/%Y")
                expiration_dates_str += date + \
                    " -------------> " + \
                    (self.type in ('out_invoice', 'in_refund') and
                     tools.formatLang(self.env, line.debit) or
                     (self.type in ('in_invoice', 'out_refund') and
                      tools.formatLang(self.env, line.credit) or "0")) + "\n"

        self.expiration_dates_str = expiration_dates_str

    expiration_dates_str = fields.Text('Expiration dates', readonly=True,
                                       compute='_get_move_lines_str')
