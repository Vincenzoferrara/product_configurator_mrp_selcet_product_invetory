from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpProductionProductSelection(models.Model):
    _name = 'mrp.production.product.selection'
    _description = 'Selezione Prodotto per Ordine di Produzione'

    production_id = fields.Many2one('mrp.production', string='Ordine di Produzione', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Prodotto Selezionato', required=True)
    qty = fields.Float(string='Quantità', default=1.0)

    def action_confirm(self):
        """Conferma la selezione del prodotto e aggiorna l'ordine di produzione"""
        for record in self:
            if not record.product_id:
                raise UserError('Devi selezionare un prodotto!')
            
            # Aggiorna l'ordine di produzione con il prodotto selezionato
            record.production_id.write({
                'product_id': record.product_id.id,
                'product_qty': record.qty,
                'product_selection_id': record.id,
            })
            
            # Ricalcola la distinta base se necessario
            record.production_id._onchange_product_id()
            
        return {'type': 'ir.actions.act_window_close'}


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    product_selection_id = fields.Many2one('mrp.production.product.selection', string='Selezione Prodotto')

    def _get_bom_from_product(self, product_id=None, bom_id=False, kit=False):
        """Override per utilizzare il prodotto selezionato"""
        if self.product_selection_id and self.product_selection_id.product_id:
            product_id = self.product_selection_id.product_id
        return super()._get_bom_from_product(product_id=product_id, bom_id=bom_id, kit=kit)
        
    @api.onchange('product_selection_id')
    def _onchange_product_selection(self):
        """Aggiorna il prodotto quando viene selezionato tramite product_selection_id"""
        for record in self:
            if record.product_selection_id and record.product_selection_id.product_id:
                record.product_id = record.product_selection_id.product_id
                record.product_qty = record.product_selection_id.qty