
# -*- coding: utf-8 -*-
{
    'name': 'Product Configurator MRP Inventory Extension',
    'version': '18.0.1.0.0',
    'category': 'Manufacturing',
    'summary': 'Extends product configurator to select products from inventory',
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'AGPL-3',
    'depends': [
        'product_configurator',
        'product_configurator_mrp',
        'mrp',
        'stock',
    ],
    'data': [
        'views/product_config_session_view.xml',
        'views/product_config_step_line_view.xml',
        'views/mrp_production_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'product_configurator_mrp_inventory/static/src/js/inventory_config_form_controller.js',
        ],
        'web.assets_qweb': [
            'product_configurator_mrp_inventory/static/src/xml/inventory_field_template.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}