{
    'name': 'Product Configurator MRP Select Product Inventory',
    'version': '1.0',
    'summary': 'Allows selecting products from inventory in MRP configurator',
    'description': """
        This module extends the product_configurator_mrp module to allow selecting
        products from inventory instead of configuring a new variant.
    """,
    'category': 'Manufacturing',
    'author': 'Your Name',
    'website': 'http://www.example.com',
    'depends': ['base', 'product_configurator_mrp', 'mrp'],
    'data': [
        'views/product_configurator_mrp_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}