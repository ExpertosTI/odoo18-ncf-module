# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class PosSession(models.Model):
    _inherit = 'pos.session'
    
    @api.model
    def _load_pos_data_models(self, config_id):
        """Registrar modelo ncf.sequence para carga en POS"""
        models = super()._load_pos_data_models(config_id)
        models.append('ncf.sequence')
        _logger.info("[NCF] Modelos POS (con ncf.sequence): %s", models)
        return models

    def load_data(self, models_to_load, only_data=False):
        if models_to_load:
            if 'ncf.sequence' not in models_to_load:
                models_to_load = list(models_to_load) + ['ncf.sequence']
        return super().load_data(models_to_load, only_data)
    
    def _loader_params_pos_config(self):
        result = super()._loader_params_pos_config()
        config_fields = result['search_params']['fields']
        fields_to_add = [
            'enable_ncf',
            'default_ncf_sequence_id',
            'customer_details',
            'customer_name',
            'customer_vat',
            'customer_phone'
        ]
        for field in fields_to_add:
            if field not in config_fields:
                config_fields.append(field)
        _logger.info("[NCF] Campos NCF añadidos a pos.config: %s", fields_to_add)
        return result
