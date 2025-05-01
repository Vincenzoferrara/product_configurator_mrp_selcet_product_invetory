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
    
    inventory_product_ids = fields.Many2many(
        'product.product',
        'mrp_production_inventory_product_rel',
        'production_id',
        'product_id',
        string='Used Inventory Products',
        help="Physical products from inventory used in this manufacturing order"
    )
    
    @api.model
    def create(self, vals):
        """Extends create method to handle inventory products in configuration"""
        res = super(MrpProduction, self).create(vals)
        
        # If the production was created from a configuration
        if res.config_session_id:
            # Check if there are inventory products in the session
            session = res.config_session_id
            
            if session.inventory_product_ids:
                res.inventory_products_used = True
                res.inventory_product_ids = [(6, 0, session.inventory_product_ids.ids)]
                
                # Get custom values that include inventory products
                custom_vals = session.get_custom_value_id()
                
                if custom_vals.get('inventory_products'):
                    # Create a temporary BOM based on the existing one
                    if res.bom_id:
                        # Copy the original BOM
                        bom = res.bom_id.copy({
                            'product_id': res.product_id.id,
                            'code': f"{res.bom_id.code or ''}-INV-{res.id}"
                        })
                        
                        # Map attributes to product categories for easier matching
                        attr_to_categ = {}
                        for attr_line in res.product_id.product_tmpl_id.attribute_line_ids:
                            if attr_line.attribute_id.category_id:
                                attr_to_categ[attr_line.attribute_id.id] = attr_line.attribute_id.category_id.id
                        
                        # Create a mapping of categories to inventory products
                        categ_to_product = {}
                        for attr_id, product_id in custom_vals['inventory_products'].items():
                            if attr_id in attr_to_categ:
                                categ_id = attr_to_categ[attr_id]
                                categ_to_product[categ_id] = product_id
                            
                        # Update BOM lines to use inventory products
                        for bom_line in bom.bom_line_ids:
                            component = bom_line.product_id
                            
                            # Try to match by product category
                            if component.categ_id.id in categ_to_product:
                                inventory_product_id = categ_to_product[component.categ_id.id]
                                inventory_product = self.env['product.product'].browse(inventory_product_id)
                                
                                if inventory_product.exists():
                                    bom_line.write({
                                        'product_id': inventory_product.id,
                                        'product_qty': 1.0  # Usually when using inventory products, quantity is 1
                                    })
                            
                            # Try to match by ingredient in product name
                            else:
                                for attr_id, product_id in custom_vals['inventory_products'].items():
                                    attribute = self.env['product.attribute'].browse(attr_id)
                                    if attribute.exists() and attribute.name.lower() in component.name.lower():
                                        inventory_product = self.env['product.product'].browse(product_id)
                                        if inventory_product.exists():
                                            bom_line.write({
                                                'product_id': inventory_product.id,
                                                'product_qty': 1.0
                                            })
                                            break
                        
                        # Use the new modified BOM
                        res.bom_id = bom.id
        
        return res
        
    def action_view_inventory_products(self):
        """Show inventory products used in this manufacturing order"""
        self.ensure_one()
        return {
            'name': _('Inventory Products'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree,form',
            'res_model': 'product.product',
            'domain': [('id', 'in', self.inventory_product_ids.ids)],
        }