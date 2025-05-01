# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductConfigSession(models.Model):
    _inherit = 'product.config.session'
    
    # Add field to store selected physical products
    inventory_product_ids = fields.Many2many(
        'product.product',
        'config_session_inventory_product_rel',
        'session_id',
        'product_id',
        string='Inventory Products'
    )
    
    # Store attribute to product mapping for selected inventory products
    inventory_product_mapping = fields.Text(
        string='Inventory Product Mapping',
        help="JSON mapping between attributes and selected inventory products"
    )
    
    @api.model
    def update_config(self, values, product_tmpl_id=None):
        """Extends update_config function to handle inventory products"""
        # Extract inventory products if present
        inventory_products = values.pop('inventory_product_ids', False)
        
        # Call original method to handle variants and other values
        result = super(ProductConfigSession, self).update_config(values, product_tmpl_id)
        
        # If there are inventory products, update them in the session
        if inventory_products and result.get('session_id'):
            session = self.browse(result.get('session_id'))
            
            # Get current mapping or initialize empty dict
            import json
            current_mapping = {}
            if session.inventory_product_mapping:
                try:
                    current_mapping = json.loads(session.inventory_product_mapping)
                except ValueError:
                    current_mapping = {}
            
            # Update mapping with new values
            for attr_id, product_id in inventory_products.items():
                if product_id:
                    current_mapping[attr_id] = product_id
                    # Also add product to many2many field
                    session.write({
                        'inventory_product_ids': [(4, int(product_id))]
                    })
            
            # Update mapping in session
            session.write({
                'inventory_product_mapping': json.dumps(current_mapping)
            })
                
        return result
    
    def get_custom_value_id(self):
        """Extends the method to include inventory products in the custom value creation"""
        result = super(ProductConfigSession, self).get_custom_value_id()
        
        # Add inventory products to the result
        if self.inventory_product_ids and self.inventory_product_mapping:
            import json
            
            # These data will be used in mrp_production to create the BOM
            if 'inventory_products' not in result:
                result['inventory_products'] = {}
            
            # Get mapping from stored json
            try:
                mapping = json.loads(self.inventory_product_mapping)
                for attr_id, product_id in mapping.items():
                    result['inventory_products'][int(attr_id)] = int(product_id)
            except (ValueError, TypeError):
                pass
                
        return result