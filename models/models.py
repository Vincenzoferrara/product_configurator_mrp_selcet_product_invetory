from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpProductionProductSelection(models.Model):
    _name = 'mrp.production.product.selection'
    _description = 'Selezione Prodotto per Ordine di Produzione'

    production_id = fields.Many2one('mrp.production', string='Ordine di Produzione', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Prodotto Selezionato', required=True)
    qty = fields.Float(string='Quantità', default=1.0)

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product_selection_id = fields.Many2one('mrp.production.product.selection', string='Selezione Prodotto')

    def _get_bom_from_product(self, product_id=None, bom_id=False, kit=False):
        if self.product_selection_id and self.product_selection_id.product_id:
            product_id = self.product_selection_id.product_id
        return super()._get_bom_from_product(product_id=product_id, bom_id=bom_id, kit=kit)