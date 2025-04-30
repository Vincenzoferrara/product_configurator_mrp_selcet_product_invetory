# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MrpConfiguratorSelectorLine(models.TransientModel):
    _name = 'product.configurator.mrp.selector.line'
    _description = 'Selector Line: choose a product by category'

    wizard_id = fields.Many2one(
        'product.configurator.mrp', required=True, ondelete='cascade'
    )
    category_id = fields.Many2one(
        'product.category', string='Category', required=True,
        help='Filter products by this category'
    )
    product_id = fields.Many2one(
        'product.product', string='Product',
        domain="[('categ_id','child_of',category_id)]",
        help='Select a stockable product from chosen category'
    )

class ProductConfiguratorMrp(models.TransientModel):
    _inherit = 'product.configurator.mrp'

    selector_line_ids = fields.One2many(
        'product.configurator.mrp.selector.line', 'wizard_id',
        string='Product Selectors',
        help='Add as many category filters as needed'
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        # Initialize with one empty selector line
        res['selector_line_ids'] = [(0, 0, {})]
        return res

    @api.onchange('selector_line_ids')
    def _onchange_selector_lines(self):
        for line in self.selector_line_ids:
            if line.category_id and not line.product_id:
                line.product_id = False

    def _get_component_values(self):
        values = super()._get_component_values()
        placeholder_map = self.env.context.get('bom_placeholder_map', {})
        for line in self.selector_line_ids:
            if line.product_id and line.category_id:
                placeholder_id = placeholder_map.get(str(line.category_id.id))
                if placeholder_id:
                    values[str(placeholder_id)] = line.product_id.id
        return values
