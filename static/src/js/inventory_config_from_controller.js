odoo.define('product_configurator_mrp_inventory.FormController', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('product_configurator.FormController');
    var session = require('web.session');
    var qweb = core.qweb;

    var _t = core._t;

    FormController.include({
        /**
         * Estende il controller del form di configurazione per supportare prodotti di inventario
         */
        _onFieldChanged: function (event) {
            var self = this;
            var result = this._super.apply(this, arguments);

            // Se siamo in una fase che usa prodotti di inventario
            var stepUseInventory = this.stepUseInventory || false;
            if (!stepUseInventory) {
                return result;
            }

            // Ottieni il valore del campo
            var field = event.data.changes;
            var fieldName = Object.keys(field)[0];
            var value = field[fieldName];

            // Se è un campo di selezione inventario
            if (fieldName.startsWith('inventory_product_')) {
                var attributeId = fieldName.split('_').pop();
                
                // Prepara i dati per l'aggiornamento della sessione
                var vals = {
                    'inventory_product_ids': {}
                };
                vals.inventory_product_ids[attributeId] = value.id;
                
                // Aggiorna la sessione con il prodotto di inventario selezionato
                this._rpc({
                    route: '/product_configurator/save_configuration',
                    params: {
                        'product_tmpl_id': this.product_tmpl_id,
                        'values': vals,
                        'session_id': this.config_session_id,
                        'config_step_id': this.config_step_id,
                    }
                }).then(function () {
                    // Potrebbe essere necessario aggiornare alcuni elementi dell'interfaccia
                    // dopo la selezione di un prodotto di inventario
                });
            }

            return result;
        },

        /**
         * Sovrascrive il metodo renderStepConfig per aggiungere campi di selezione prodotti da inventario
         */
        renderStepConfig: function (data) {
            var self = this;
            var result = this._super.apply(this, arguments);
            
            // Verifica se questa fase usa prodotti di inventario
            this.stepUseInventory = data.config_step_line && data.config_step_line.use_inventory_products;
            
            if (this.stepUseInventory) {
                // Per ogni attributo, aggiungi un campo di selezione prodotti
                _.each(data.attribute_lines, function (attrLine) {
                    // Crea un campo di selezione prodotti di inventario
                    var fieldName = 'inventory_product_' + attrLine.attribute_id;
                    
                    // Ottieni i prodotti disponibili per questo attributo
                    self._rpc({
                        model: 'product.config.step.line',
                        method: 'get_available_inventory_products',
                        args: [data.config_step_line.id, attrLine.attribute_id],
                    }).then(function (products) {
                        // Crea e inserisci il campo di selezione dopo l'attributo corrispondente
                        var $attrField = self.$('[name="' + attrLine.attribute_id + '"]');
                        if ($attrField.length) {
                            var $inventoryField = $(qweb.render('ProductConfiguratorInventoryField', {
                                products: products,
                                fieldName: fieldName,
                                attributeName: attrLine.attribute_name
                            }));
                            
                            $inventoryField.insertAfter($attrField.closest('.form-group'));
                            
                            // Gestisce il change dell'elemento
                            $inventoryField.find('select').on('change', function(e) {
                                var fieldObj = {};
                                fieldObj[fieldName] = {
                                    id: parseInt($(this).val()),
                                    display_name: $(this).find('option:selected').text()
                                };
                                
                                self._onFieldChanged({
                                    data: {
                                        changes: fieldObj
                                    }
                                });
                            });
                        }
                    });
                });
            }
            
            return result;
        }
    });

    return FormController;
});