# -*- coding: utf-8 -*-
# © 2017 Savoir-faire Linux
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

{
    'name': 'Secure Accounting',
    'version': '10.0.1.0.0',
    'author': 'Savoir-faire Linux',
    'maintainer': 'Savoir-faire Linux',
    'website': 'http://www.savoirfairelinux.com',
    'license': 'LGPL-3',
    'category': 'Accounting & Finance',
    'depends': [
        'account',
    ],
    'data': [
        'security/res_groups.xml',
        'security/ir.model.access.csv',
    ],
    'application': False,
    'installable': True,
}
