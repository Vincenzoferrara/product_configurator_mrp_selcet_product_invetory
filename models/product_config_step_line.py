# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductConfigStepLine(models.Model):
    _inherit = 'product.config.step.line'
    
    use_inventory_products = fields.Boolean(
        string='Use Inventory Products',
        default=False,
        help="If checked, this step will use physical products from inventory instead of product variants"
    )
    
    inventory_product_domain = fields.Char(
        string='Inventory Products Domain',
        default="[('qty_available', '>', 0)]",
        help="Domain to filter available inventory products"
    )
    
    def get_available_inventory_products(self, attribute_id=None):
        """
        Restituisce i prodotti disponibili nell'inventario per un attributo
        """
        self.ensure_one()
        
        if not self.use_inventory_products:
            return []
            
        domain = eval(self.inventory_product_domain or "[]")
        
        # Se è specificato un attributo, filtra ulteriormente
        if attribute_id:
            attribute = self.env['product.attribute'].browse(attribute_id)
            if attribute.category_id:
                # Esempio: filtra prodotti per categoria corrispondente all'attributo
                domain += [('categ_id', 'child_of', attribute.category_id.name)]
                
        return self.env['product.product'].search(domain)