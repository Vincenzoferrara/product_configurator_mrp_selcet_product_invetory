from odoo import models, fields, api

class ProductConfigurator(models.Model):
    _inherit = 'product.configurator'

    inventory_location_id = fields.Many2one('stock.location', string='Inventory Location', domain="[('usage', '=', 'internal')]")

    @api.onchange('inventory_location_id')
    def _onchange_inventory_location_id(self):
        # Aggiungi qui la logica per gestire la selezione della posizione dell'inventario
        pass