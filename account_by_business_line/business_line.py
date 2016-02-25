# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2013
#    Pexego Sistemas Informáticos (http://www.pexego.es)
#    Copyright (C) 2015
#    Comunitea Servicios Tecnológicos (http://www.comunitea.com)
#    $Omar Castiñeira Saavedra$
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

from openerp.osv import orm, fields

class account_business_line(orm.Model):

    _name = "account.business.line"

    _columns = {
        'name': fields.char('Name', size=128, required=True),
        'description': fields.text('Description')
    }


