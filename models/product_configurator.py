from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ProductConfiguratorWizard(models.TransientModel):
    _inherit = 'product.configurator.wizard'

    qty_available = fields.Float(string='Quantità Disponibile', readonly=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.qty_available = self.product_id.qty_available
        else:
            self.qty_available = 0.0

    def action_add_to_cart(self):
        """Aggiunge il prodotto al carrello se la quantità è disponibile."""
        if self.qty > self.qty_available:
            raise ValidationError("La quantità richiesta non è disponibile in magazzino.")
        return super(ProductConfiguratorWizard, self).action_add_to_cart()

    # Esempio di funzione per controllare la disponibilità (opzionale)
    # def action_check_availability(self):
    #     """Verifica la disponibilità del prodotto."""
    #     if self.product_id and self.qty > self.qty_available:
    #         raise ValidationError("La quantità richiesta non è disponibile in magazzino.")
    #     else:
    #         return {
    #             'type': 'ir.actions.client',
    #             'tag': 'display_notification',
    #             'params': {
    #                 'title': 'Disponibilità',
    #                 'message': 'La quantità richiesta è disponibile.',
    #                 'type': 'success',
    #                 'sticky': False,
    #             }
    #         }