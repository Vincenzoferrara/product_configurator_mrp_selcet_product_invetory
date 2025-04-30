from odoo import fields, models

class ProductQty(models.TransientModel):
    _name = 'product.qty'
    _description = 'Product Quantity'

    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Prodotto',
        required=True
    )
    qty = fields.Float(
        string='Quantità',
        default=1.0,
        required=True
    )
    config_id = fields.Many2one(
        comodel_name='product.configurator.mrp',
        string='Configurazione'
    )
