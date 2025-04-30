from odoo import models, fields, api
from odoo.exceptions import UserError

class ProductConfiguratorMrpProduct(models.TransientModel):
    _name = 'product.configurator.mrp.product'
    _description = 'Seleziona Prodotto da Magazzino'

    config_id = fields.Many2one('product.configurator.mrp', string='Configurazione', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Prodotto', required=True, domain="[('type', '=', 'product')]")
    qty = fields.Float(string='Quantità', default=1.0)

class ProductConfiguratorMrp(models.Model):
    _inherit = 'product.configurator.mrp'

    product_id = fields.Many2one('product.product', string='Prodotto Selezionato')
    qty = fields.Float(string='Quantità', default=1.0)

    def _create_production_order(self):
        # Controlla se è stato selezionato un prodotto
        if self.product_id:
            # Crea l'ordine di produzione con il prodotto selezionato
            bom = self.env['mrp.bom']._bom_find(product=self.product_id)
            if not bom:
                raise UserError("Nessuna distinta base trovata per questo prodotto.")

            production = self.env['mrp.production'].create({
                'product_id': self.product_id.id,
                'product_qty': self.qty,
                'product_uom_id': self.product_id.uom_id.id,
                'bom_id': bom.id,
                'origin': self.display_name,
                'company_id': self.company_id.id,
            })
            return production
        else:
            # Chiama il metodo originale se non è stato selezionato un prodotto
            return super()._create_production_order()