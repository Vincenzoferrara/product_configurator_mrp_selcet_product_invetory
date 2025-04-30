{
    'name': 'MRP Configurator: On-the-fly Product Selectors',
    'version': '18.0.1.0.0',
    'author': 'Your Name',
    'category': 'Manufacturing',
    'summary': 'Allow adding multiple category-based product selectors directly in the Manufacturing Configurator wizard',
    'depends': ['base', 'product_configurator_mrp'],
    'data': [
        'views/product_selector_view.xml',
    ],
    'installable': True,
    'application': False,
}
