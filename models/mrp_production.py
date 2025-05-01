# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class MrpProduction(models.Model):
    _inherit = 'mrp.production'
    
    inventory_products_used = fields.Boolean(
        string='Used Inventory Products',
        default=False,
        help="Indicates if this MO used physical inventory products in its configuration"
    )
    
    @api.model
    def create(self, vals):
        """Estende il metodo create per gestire prodotti di inventario nella configurazione"""
        res = super(MrpProduction, self).create(vals)
        
        # Se la produzione è stata creata da una configurazione
        if res.config_session_id:
            # Verifica se ci sono prodotti di inventario nella sessione
            if res.config_session_id.inventory_product_ids:
                res.inventory_products_used = True
                
                # Se esiste già una BOM, ma vogliamo modificarla per usare prodotti fisici
                if res.bom_id:
                    # Ottieni i valori custom che includono i prodotti di inventario
                    custom_vals = res.config_session_id.get_custom_value_id()
                    
                    if 'inventory_products' in custom_vals:
                        # Crea una BOM temporanea basata su quella esistente
                        bom = res.bom_id.copy()
                        bom.write({'product_id': res.product_id.id})
                        
                        # Modifica le linee della BOM per utilizzare i prodotti fisici
                        for bom_line in bom.bom_line_ids:
                            # Cerca il prodotto di inventario corrispondente
                            for attr_line in res.product_id.attribute_line_ids:
                                if attr_line.attribute_id.id in custom_vals['inventory_products']:
                                    product_id = custom_vals['inventory_products'][attr_line.attribute_id.id]
                                    inventory_product = self.env['product.product'].browse(product_id)
                                    
                                    # Se il componente corrisponde all'attributo, sostituiscilo
                                    if bom_line.product_id.categ_id == inventory_product.categ_id:
                                        bom_line.write({'product_id': inventory_product.id})
                        
                        # Usa la nuova BOM modificata
                        res.bom_id = bom.id
        
        return res