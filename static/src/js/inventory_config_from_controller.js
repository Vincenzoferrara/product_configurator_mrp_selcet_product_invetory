odoo.define('product_configurator_mrp_inventory.FormController', function (require) {
    "use strict";

    var core = require('web.core');
    var FormController = require('product_configurator.FormController');
    var session = require('web.session');
    var qweb = core.qweb;

    var _t = core._t;

    FormController.include({
        /**
         * Extends the configuration form controller to support inventory products
         */
        _onFieldChanged: function (event) {
            var self = this;
            var result = this._super.apply(this, arguments);

            // If we are in a step that uses inventory products
            var stepUseInventory = this.stepUseInventory || false;
            if (!stepUseInventory) {
                return result;
            }

            // Get the field value
            var field = event.data.changes;
            var fieldName = Object.keys(field)[0];
            var value = field[fieldName];

            // If it's an inventory selection field
            if (fieldName.startsWith('inventory_product_')) {
                var attributeId = fieldName.split('_').pop();
                
                // Prepare data for session update
                var vals = {
                    'inventory_product_ids': {}
                };
                vals.inventory_product_ids[attributeId] = value.id;
                
                // Update session with selected inventory product
                this._rpc({
                    route: '/product_configurator/save_configuration',
                    params: {
                        'product_tmpl_id': this.product_tmpl_id,
                        'values': vals,
                        'session_id': this.config_session_id,
                        'config_step_id': this.config_step_id,
                    }
                }).then(function () {
                    // We might need to update some UI elements
                    // after selecting an inventory product
                });
            }

            return result;
        },

        /**
         * Overrides renderStepConfig to add inventory product selection fields
         */
        renderStepConfig: function (data) {
            var self = this;
            var result = this._super.apply(this, arguments);
            
            // Check if this step uses inventory products
            this.stepUseInventory = data.config_step_line && data.config_step_line.use_inventory_products;
            
            if (this.stepUseInventory) {
                // For each attribute, add a product selection field
                _.each(data.attribute_lines, function (attrLine) {
                    // Create an inventory product selection field
                    var fieldName = 'inventory_product_' + attrLine.attribute_id;
                    
                    // Get available products for this attribute
                    self._rpc({
                        model: 'product.config.step.line',
                        method: 'get_available_inventory_products',
                        args: [data.config_step_line.id, attrLine.attribute_id],
                    }).then(function (products) {
                        // Create and insert the selection field after the corresponding attribute
                        var $attrField = self.$('[name="' + attrLine.attribute_id + '"]');
                        if ($attrField.length) {
                            var $inventoryField = $(qweb.render('ProductConfiguratorInventoryField', {
                                products: products,
                                fieldName: fieldName,
                                attributeName: attrLine.attribute_name
                            }));
                            
                            $inventoryField.insertAfter($attrField.closest('.form-group'));
                            
                            // Handle change event
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