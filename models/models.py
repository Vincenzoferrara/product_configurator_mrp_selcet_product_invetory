from odoo import models, fields, api

class ProductConfiguratorMrp(models.Model):
    _name = 'product.configurator.mrp'
    _description = 'Configurazione MRP'

    product_template_id = fields.Many2one('product.template', string='Modello Prodotto', required=True)
    product_qty_ids = fields.One2many('product.configurator.mrp.qty', 'config_id', string='Prodotti e Quantità')

class ProductConfiguratorMrpQty(models.Model):
    _name = 'product.configurator.mrp.qty'
    _description = 'Quantità Prodotto Configurazione MRP'

    product_id = fields.Many2one('product.product', string='Prodotto', required=True)
    qty = fields.Float(string='Quantità', required=True)
    config_id = fields.Many2one('product.configurator.mrp', string='Configurazione', required=True, ondelete='cascade')