{
    'name': 'Product Configurator MRP Select Product Inventory',
    'version': '18.1.0.0',
    'category': 'Product',
    'summary': 'Adds inventory selection to product configurator MRP',
    'author': 'Vincenzo Ferrara',
    'website': 'https://www.example.com',
    'license': 'AGPL-3',  # Aggiunta della licenza
    'depends': ['product_configurator_mrp', 'product_configurator', 'stock'],
    'data': [
        'views/product_configurator_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}