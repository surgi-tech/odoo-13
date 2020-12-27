# -*- coding: utf-8 -*-
{
    'name': "surgi_invoice_addons",

    'summary': """
        control Invoice Module""",

    'description': """
        1- add compination product to the invoice page
    """,

    'author': "Ahmed Abd Al Aziz",
    'website': "",


    'category': 'Invoicing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','product','account'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'views/compine_product.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
