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
        Returns available inventory products for an attribute
        """
        self.ensure_one()
        
        if not self.use_inventory_products:
            return []
            
        domain = eval(self.inventory_product_domain or "[]")
        
        # If an attribute is specified, filter further
        if attribute_id:
            attribute = self.env['product.attribute'].browse(attribute_id)
            if attribute.exists():
                # Get attribute values for additional filtering
                attr_values = self.env['product.template.attribute.line'].search([
                    ('attribute_id', '=', attribute_id),
                    ('product_tmpl_id', '=', self.product_tmpl_id.id)
                ]).value_ids
                
                # First try: match by product category linked to the attribute
                if attribute.category_id:
                    domain.append(('categ_id', 'child_of', attribute.category_id.id))
                
                # Second try: match products that have attribute values in their name
                # This is a simple heuristic that might need customization based on actual naming conventions
                if attr_values:
                    or_conditions = []
                    for val in attr_values:
                        or_conditions.append(('name', 'ilike', val.name))
                    if or_conditions:
                        domain.append('|')
                        domain.extend(or_conditions)
        
        return self.env['product.product'].search_read(domain, ['id', 'name', 'qty_available', 'default_code'])