# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductConfigSession(models.Model):
    _inherit = 'product.config.session'
    
    # Aggiungi un campo per memorizzare i prodotti fisici selezionati
    inventory_product_ids = fields.Many2many(
        'product.product',
        'config_session_inventory_product_rel',
        'session_id',
        'product_id',
        string='Inventory Products'
    )
    
    # Estendi la funzione di aggiornamento valori per supportare i prodotti di inventario
    @api.model
    def update_config(self, values, product_tmpl_id=None):
        """Estende la funzione update_config per considerare i prodotti fisici"""
        # Estrai i prodotti di inventario se presenti
        inventory_products = values.pop('inventory_product_ids', False)
        
        # Chiama il metodo originale per gestire le varianti e altri valori
        result = super(ProductConfigSession, self).update_config(values, product_tmpl_id)
        
        # Se ci sono prodotti di inventario, aggiornali nella sessione
        if inventory_products:
            session = self.browse(result.get('session_id'))
            # Converti i prodotti in un formato compatibile con il campo Many2many
            product_ids = []
            for attr, product_id in inventory_products.items():
                if product_id:
                    product_ids.append(int(product_id))
            
            if product_ids:
                session.write({'inventory_product_ids': [(6, 0, product_ids)]})
                
        return result
    
    def get_custom_value_id(self):
        """Estende il metodo per considerare i prodotti di inventario nella creazione del valore personalizzato"""
        result = super(ProductConfigSession, self).get_custom_value_id()
        
        # Se abbiamo prodotti di inventario, aggiungiamoli al risultato
        if self.inventory_product_ids:
            # Questi dati verranno utilizzati in mrp_production per creare la BOM
            if 'inventory_products' not in result:
                result['inventory_products'] = {}
                
            # Associa ogni prodotto all'attributo corrispondente
            for config_line in self.config_step_line_id.attribute_line_ids:
                # Cerca se c'è un prodotto selezionato per questo attributo
                for product in self.inventory_product_ids:
                    # Qui dovresti implementare la logica per associare il prodotto all'attributo
                    # Ad esempio, potresti basarti su una categoria o su una proprietà specifica
                    # Per ora usiamo un esempio semplificato
                    
                    # Esempio: associa il prodotto all'attributo se hanno la stessa categoria
                    if config_line.attribute_id.category_id and product.categ_id.name == config_line.attribute_id.category_id.name:
                        result['inventory_products'][config_line.attribute_id.id] = product.id
                        
        return result