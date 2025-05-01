{
    'name': 'Product Configurator MRP Select Product Inventory',
    'version': '18.0.1.0',
    'category': 'Manufacturing',
    'summary': 'Adds inventory selection to product configurator MRP',
    'author': 'Vincenzo Ferrara',
    'website': 'https://www.example.com',
    'license': 'AGPL-3',  # Aggiunta della licenza
    'depends': ['product_configurator_mrp', 'product_configurator'],
    'data': [
        'security/ir.model.access.csv',  # Importante per i permessi
        'views/product_configurator_views.xml',
        'views/product_configurator_actions.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}