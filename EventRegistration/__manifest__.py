# -*- coding: utf-8 -*-
{
    'name':        "EventRegistration",

    'summary':
                   """
                   
                   """,

    'description': """
       
    """,

    'author':      "Ahmed Abd Al Aziz",
    'website':     "https://it-v.odoo.com/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category':    '',
    'version':     '0.1',

    # any module necessary for this one to work correctly
    'depends':     ['base','website','event'],

    # always loaded
    'data':        [
        "security/ir.model.access.csv",
        "views/front.xml",
        "views/menus.xml",
    ],
    # only loaded in demonstration mode
    'demo':        [],
    'license': 'AGPL-3',
}
