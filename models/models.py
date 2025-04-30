from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product_id = fields.Many2one('product.product', string='Prodotto Selezionato')
    qty = fields.Float(string='Quantità', default=1.0)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.product_qty = 1.0
            self.product_uom_id = self.product_id.uom_id.id

    def _update_raw_move(self, bom_line, line_data):
        self.ensure_one()
        if self.product_id:
            line_data['product_id'] = self.product_id.id
        return super()._update_raw_move(bom_line, line_data)