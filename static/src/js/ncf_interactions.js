odoo.define('ncf.interactions', function (require) {
    'use strict';

    var FormController = require('web.FormController');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var _t = core._t;

    FormController.include({
        /**
         * Mejoras para el módulo NCF
         */
        _onButtonClicked: function (event) {
            var self = this;
            var attrs = event.data.attrs;
            
            // Mejorar feedback visual para botones NCF
            if (attrs.name === 'toggle_use_ncf') {
                this._handleNCFToggle(event);
                return;
            }
            
            if (attrs.name === 'action_apply' && this.modelName === 'ncf.sequence.wizard') {
                this._handleNCFAssignment(event);
                return;
            }
            
            return this._super.apply(this, arguments);
        },

        /**
         * Maneja el toggle de NCF con feedback visual mejorado
         */
        _handleNCFToggle: function (event) {
            var self = this;
            var $button = $(event.target);
            
            // Agregar estado de loading
            $button.addClass('o_loading').prop('disabled', true);
            
            // Ejecutar la acción original
            this._super.apply(this, arguments).then(function (result) {
                $button.removeClass('o_loading').prop('disabled', false);
                
                // Mostrar notificación de éxito
                if (result && result.type === 'ir.actions.act_window') {
                    self.displayNotification({
                        type: 'info',
                        title: _t('NCF'),
                        message: _t('Abriendo wizard de selección de NCF...'),
                        sticky: false
                    });
                } else {
                    self.displayNotification({
                        type: 'success',
                        title: _t('NCF'),
                        message: _t('NCF desactivado correctamente'),
                        sticky: false
                    });
                }
            }).catch(function (error) {
                $button.removeClass('o_loading').prop('disabled', false);
                self.displayNotification({
                    type: 'danger',
                    title: _t('Error'),
                    message: error.message || _t('Error al procesar la solicitud'),
                    sticky: true
                });
            });
        },

        /**
         * Maneja la asignación de NCF con validaciones
         */
        _handleNCFAssignment: function (event) {
            var self = this;
            var $button = $(event.target);
            var record = this.model.get(this.handle);
            
            // Validar que se haya seleccionado una secuencia
            if (!record.data.ncf_sequence_id) {
                this.displayNotification({
                    type: 'warning',
                    title: _t('Advertencia'),
                    message: _t('Debe seleccionar una secuencia NCF antes de continuar'),
                    sticky: false
                });
                return;
            }
            
            // Agregar estado de loading
            $button.addClass('o_loading').prop('disabled', true);
            
            // Ejecutar la acción original
            this._super.apply(this, arguments).then(function (result) {
                $button.removeClass('o_loading').prop('disabled', false);
                
                self.displayNotification({
                    type: 'success',
                    title: _t('NCF'),
                    message: _t('NCF asignado correctamente'),
                    sticky: false
                });
            }).catch(function (error) {
                $button.removeClass('o_loading').prop('disabled', false);
                self.displayNotification({
                    type: 'danger',
                    title: _t('Error'),
                    message: error.message || _t('Error al asignar NCF'),
                    sticky: true
                });
            });
        }
    });

    // Mejoras para campos NCF
    var FieldChar = require('web.basic_fields').FieldChar;
    
    var NCFField = FieldChar.extend({
        /**
         * Campo especializado para NCF con validación en tiempo real
         */
        _onInput: function () {
            this._super.apply(this, arguments);
            
            if (this.name === 'ncf') {
                this._validateNCFFormat();
            }
        },

        _validateNCFFormat: function () {
            var value = this.$input.val();
            var $field = this.$el;
            
            if (value) {
                // Formato básico NCF: 3 caracteres + 8 dígitos
                var ncfRegex = /^[A-Z]\d{2}\d{8}$/;
                
                if (ncfRegex.test(value)) {
                    $field.removeClass('o_field_invalid').addClass('o_field_valid');
                    this._showTooltip('✅ Formato NCF válido', 'success');
                } else {
                    $field.removeClass('o_field_valid').addClass('o_field_invalid');
                    this._showTooltip('❌ Formato NCF inválido. Debe ser: Letra + 2 dígitos + 8 dígitos', 'error');
                }
            } else {
                $field.removeClass('o_field_invalid o_field_valid');
            }
        },

        _showTooltip: function (message, type) {
            var self = this;
            var $tooltip = $('<div class="ncf-tooltip ' + type + '">' + message + '</div>');
            
            this.$el.append($tooltip);
            
            setTimeout(function () {
                $tooltip.fadeOut(function () {
                    $tooltip.remove();
                });
            }, 3000);
        }
    });

    // Registrar el campo personalizado
    var fieldRegistry = require('web.field_registry');
    fieldRegistry.add('ncf_field', NCFField);

    // Mejoras para el wizard
    var AbstractAction = require('web.AbstractAction');
    
    var NCFWizardEnhancements = AbstractAction.extend({
        init: function () {
            this._super.apply(this, arguments);
            this._addKeyboardShortcuts();
        },

        _addKeyboardShortcuts: function () {
            var self = this;
            
            // Atajo Ctrl+Enter para aplicar
            $(document).on('keydown.ncf_wizard', function (e) {
                if (e.ctrlKey && e.keyCode === 13) {
                    var $applyBtn = $('.btn-primary[name="action_apply"]');
                    if ($applyBtn.length && !$applyBtn.prop('disabled')) {
                        $applyBtn.click();
                    }
                }
                
                // Escape para cancelar
                if (e.keyCode === 27) {
                    var $cancelBtn = $('.btn-secondary[special="cancel"]');
                    if ($cancelBtn.length) {
                        $cancelBtn.click();
                    }
                }
            });
        },

        destroy: function () {
            $(document).off('keydown.ncf_wizard');
            this._super.apply(this, arguments);
        }
    });

    return {
        NCFField: NCFField,
        NCFWizardEnhancements: NCFWizardEnhancements
    };
});

// CSS adicional para tooltips
odoo.define('ncf.tooltip_styles', function (require) {
    'use strict';
    
    var styles = `
        <style>
            .ncf-tooltip {
                position: absolute;
                top: -30px;
                left: 50%;
                transform: translateX(-50%);
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                z-index: 1000;
                white-space: nowrap;
                animation: fadeInOut 3s ease-in-out;
            }
            
            .ncf-tooltip.success {
                background-color: #28a745;
                color: white;
            }
            
            .ncf-tooltip.error {
                background-color: #dc3545;
                color: white;
            }
            
            @keyframes fadeInOut {
                0%, 100% { opacity: 0; }
                10%, 90% { opacity: 1; }
            }
            
            .o_field_valid {
                border-color: #28a745 !important;
                box-shadow: 0 0 0 0.2rem rgba(40, 167, 69, 0.25);
            }
        </style>
    `;
    
    $('head').append(styles);
});