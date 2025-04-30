from odoo import models, fields, api

class ProductConfiguratorMrpSelectProductInventory(models.Model):
    _name = 'product.configurator.mrp.select.product.inventory'
    _description = 'Prodotti dal Magazzino per Configurazione MRP'

    config_id = fields.Many2one('product.configurator.mrp', string='Configurazione', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Prodotto', required=True)
    qty = fields.Float(string='Quantità', required=True)

class ProductConfiguratorMrp(models.Model):
    _inherit = 'product.configurator.mrp'

    product_inventory_ids = fields.One2many('product.configurator.mrp.select.product.inventory', 'config_id', string='Prodotti dal Magazzino')
