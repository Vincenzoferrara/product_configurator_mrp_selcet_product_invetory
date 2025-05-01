from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ProductConfiguratorWizard(models.TransientModel):
    _inherit = 'product.configurator.wizard'

    qty_available = fields.Float(
        string='Quantity Available',
        readonly=True,
        help='Available quantity in stock',
    )

    @api.onchange('product_id')
    def _onchange_product_id(self):
        """Update qty_available when product_id changes."""
        if self.product_id:
            self.qty_available = self.product_id.qty_available
        else:
            self.qty_available = 0.0

    def action_add_to_cart(self):
        """Add the product to the cart if the quantity is available."""
        self.ensure_one()
        if self.qty > self.qty_available:
            raise ValidationError("The requested quantity is not available in stock.")
        return super().action_add_to_cart()