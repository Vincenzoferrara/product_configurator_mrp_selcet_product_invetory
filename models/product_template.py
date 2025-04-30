from odoo import fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_category_id = fields.Many2one(
        comodel_name='product.category',
        string='Categoria Prodotto',
        help='Categoria di prodotti consentiti per questo template.'
    )
