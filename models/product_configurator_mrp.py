from odoo import fields, models

class ProductConfiguratorMrp(models.TransientModel):
    _inherit = "product.configurator.mrp"

    product_template_id = fields.Many2one(
        comodel_name='product.template',
        string='Template Prodotto',
        required=True,
        domain="[('config_ok', '=', True)]",  # Filtra solo i template configurabili
        help='Template di prodotto da utilizzare per creare la distinta base.'
    )

    product_qty_ids = fields.One2many(
        comodel_name="product.qty",
        inverse_name="config_id",
        string="Prodotti e Quantità",
    )

    def action_config_done(self):
        # Recupera i prodotti e le quantità selezionate
        product_qty_list = [(product.product_id.id, product.qty) for product in self.product_qty_ids]

        # Recupera il template selezionato
        product_template = self.product_template_id

        # Crea la distinta base con i prodotti selezionati
        # (Qui dovrai implementare la logica per creare la distinta base)
        # Esempio:
        bom_vals = {
            'product_tmpl_id': product_template.id,
            'product_qty': 1.0,  # Quantità del prodotto principale
            'type': 'normal',  # Tipo di distinta base
            'bom_line_ids': [(0, 0, {'product_id': product_id, 'product_qty': qty}) for product_id, qty in product_qty_list],
        }
        bom = self.env['mrp.bom'].create(bom_vals)

        # Aggiorna l'ordine di produzione (se esiste)
        if self.order_id:
            # Aggiorna l'ordine con i prodotti selezionati
            self.order_id.write({'bom_id': bom.id})
        else:
            # Crea un nuovo ordine di produzione
            mrp_vals = {
                'product_id': product_template.product_variant_id.id,  # Prodotto principale
                'product_qty': 1.0,  # Quantità da produrre
                'bom_id': bom.id,
                'product_uom_id': product_template.uom_id.id,
            }
            mrp_order = self.env['mrp.production'].create(mrp_vals)

        # Restituisci l'azione per visualizzare l'ordine di produzione
        action = self.env["ir.actions.actions"]._for_xml_id("mrp.mrp_production_action")
        action['res_id'] = mrp_order.id
        return action
