# -*- coding: utf-8 -*-
# © 2017 Comunitea
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    'name': 'Website facebook pixel',
    'summary': '',
    'version': '8.0.1.0.0',
    'category': 'Website',
    'website': 'comunitea.com',
    'author': 'Comunitea',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'depends': [
        'base',
        'website_sale',
        'payment_redsys',
    ],
    'data': [
        'views/website.xml'
    ],
}
