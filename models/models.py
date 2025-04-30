from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    # Campo per indicare se selezionare un prodotto dall'inventario
    use_inventory_product = fields.Boolean(string='Usa Prodotto da Inventario', default=False)
    inventory_product_id = fields.Many2one('product.product', string='Prodotto da Inventario')
    
    @api.onchange('use_inventory_product', 'inventory_product_id')
    def _onchange_inventory_product(self):
        """Aggiorna il prodotto quando viene selezionato dall'inventario"""
        for record in self:
            if record.use_inventory_product and record.inventory_product_id:
                record.product_id = record.inventory_product_id
    
    def _get_bom_from_product(self, product_id=None, bom_id=False, kit=False):
        """Override per utilizzare il prodotto selezionato dall'inventario"""
        if self.use_inventory_product and self.inventory_product_id:
            product_id = self.inventory_product_id
        return super()._get_bom_from_product(product_id=product_id, bom_id=bom_id, kit=kit)


class ProductConfiguratorMrp(models.TransientModel):
    _inherit = 'product.configurator.mrp'
    
    # Aggiungiamo un'opzione per selezionare un prodotto esistente
    use_inventory_product = fields.Boolean(string='Usa Prodotto da Inventario', default=False)
    inventory_product_id = fields.Many2one('product.product', string='Prodotto da Inventario')
    
    @api.onchange('use_inventory_product')
    def _onchange_use_inventory_product(self):
        """Svuota il campo del prodotto dall'inventario se l'opzione è disattivata"""
        if not self.use_inventory_product:
            self.inventory_product_id = False
    
    @api.onchange('inventory_product_id')
    def _onchange_inventory_product(self):
        """Disattiva la configurazione del prodotto se viene selezionato un prodotto dall'inventario"""
        if self.inventory_product_id:
            self.use_inventory_product = True
    
    def create_mrp_production(self):
        """Override per utilizzare il prodotto selezionato dall'inventario"""
        if self.use_inventory_product and self.inventory_product_id:
            # Se viene selezionato un prodotto dall'inventario, utilizziamo quello anziché configurare
            production = self.env['mrp.production'].create({
                'product_id': self.inventory_product_id.id,
                'product_qty': self.quantity,
                'product_uom_id': self.inventory_product_id.uom_id.id,
                'bom_id': self._get_bom_id_from_product(self.inventory_product_id),
                'use_inventory_product': True,
                'inventory_product_id': self.inventory_product_id.id,
            })
            
            # Propagazione onchange per il calcolo della distinta base e dei componenti
            production._onchange_product_id()
            production._onchange_bom_id()
            production._onchange_move_raw()
            
            return {
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'view_mode': 'form',
                'res_id': production.id,
            }
        else:
            # Altrimenti, esegui il comportamento predefinito
            return super().create_mrp_production()
    
    def _get_bom_id_from_product(self, product):
        """Ottiene la distinta base appropriata per il prodotto"""
        bom = self.env['mrp.bom'].search([
            '|',
            ('product_id', '=', product.id),
            '&',
            ('product_id', '=', False),
            ('product_tmpl_id', '=', product.product_tmpl_id.id)
        ], limit=1)
        return bom.id if bom else False