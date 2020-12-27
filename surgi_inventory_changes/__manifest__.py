{
    'name': 'Surgitech Inventory',
    'version': '10.0.0.1',
    'author': 'Ahmed Salama , Zienab Abd EL Nasser',
    'category': 'Inventory',
    'description': """
Warehouse modifications
==========================
    """,
    'depends': ['stock','surgi_product_template','sale'],
    'data': [
        'views/stock_picking_changes_view.xml',
        'views/stock_picking_type_changes_view.xml',
        'views/stock_warehouse_view_changes.xml',
        'views/stock_location_changes_view.xml',
        'views/stock_warehouse_changes_view.xml',
        'views/sale.order.xml',
        'security/ir.model.access.csv',
        'security/stock_inventory_security.xml',
    ],
}
