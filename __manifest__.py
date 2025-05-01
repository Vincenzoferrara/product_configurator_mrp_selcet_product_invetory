{
    'name': 'Product Configurator MRP Select Product Inventory',
    'version': '1.0',
    'summary': 'Adds inventory selection to product configurator MRP',
    'description': """
        This module adds the ability to select products based on available inventory
        in the product configurator MRP.
    """,
    'category': 'Product',
    'author': 'Vincenzo Ferrara',
    'website': 'https://www.example.com',
    'depends': ['product_configurator_mrp', 'stock'],  # Dipende da product_configurator_mrp e stock
    'data': [
        'views/product_configurator_views.xml',  # Definisce le viste
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}