# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import date
import logging

_logger = logging.getLogger(__name__)

class PosOrder(models.Model):
    _inherit = 'pos.order'
    
    ncf = fields.Char(
        string='NCF',
        size=19,
        copy=False,
        index=True
    )
    
    ncf_type = fields.Char(
        string='Tipo NCF',
        size=2
    )
    
    ncf_expiration_date = fields.Date(
        string='Válido Hasta',
        copy=False,
        help='Fecha de validez del NCF para fines de impresión en POS'
    )
    
    
    @api.model
    def _order_fields(self, ui_order):
        order_fields = super()._order_fields(ui_order)
        if ui_order.get('ncf_type'):
            order_fields['ncf_type'] = ui_order['ncf_type']
        else:
            order_fields['ncf_type'] = '02'
        # Accept NCF coming from POS (allocated client-side)
        if ui_order.get('ncf'):
            order_fields['ncf'] = ui_order['ncf']
        # Accept and sanitize expiration date from UI
        exp = ui_order.get('ncf_expiration_date')
        if exp:
            if isinstance(exp, str) and exp.lower() == 'null':
                order_fields['ncf_expiration_date'] = False
            else:
                try:
                    order_fields['ncf_expiration_date'] = fields.Date.to_date(exp)
                except Exception:
                    order_fields['ncf_expiration_date'] = False
        _logger.info("[NCF] _order_fields - Tipo NCF recibido: %s", order_fields.get('ncf_type'))
        return order_fields
    
    @api.model_create_multi
    def create(self, vals_list):
        _logger.info("[NCF] create - vals_list: %s", vals_list)
        
        # Generar NCF ANTES de crear la orden
        for vals in vals_list:
            # Sanear expiración si viene como cadena 'null'
            if isinstance(vals.get('ncf_expiration_date'), str):
                if vals['ncf_expiration_date'].lower() == 'null' or vals['ncf_expiration_date'].strip() == '':
                    vals['ncf_expiration_date'] = False
            if not vals.get('ncf'):
                session_id = vals.get('session_id')
                if session_id:
                    session = self.env['pos.session'].browse(session_id)
                    if session.config_id.enable_ncf:
                        ncf_type = vals.get('ncf_type', '02')
                        sequence = self.env['ncf.sequence'].search([
                            ('company_id', '=', session.company_id.id),
                            ('ncf_type', '=', ncf_type),
                            ('active', '=', True)
                        ], limit=1)
                        
                        if sequence:
                            vals['ncf'] = sequence._next()
                            # Alinear con facturas: vencer al final del año fiscal vigente
                            today = date.today()
                            vals['ncf_expiration_date'] = date(today.year, 12, 31)
                            _logger.info("[NCF] Generado %s para nueva orden (tipo %s)", vals['ncf'], ncf_type)
                        else:
                            _logger.warning("[NCF] No se encontró secuencia activa para tipo %s", ncf_type)
            else:
                # Si NCF viene desde UI sin expiración válida, completar en servidor
                if not vals.get('ncf_expiration_date'):
                    today = date.today()
                    vals['ncf_expiration_date'] = date(today.year, 12, 31)
        
        orders = super().create(vals_list)
        return orders
    
    def _export_for_ui(self, order):
        result = super()._export_for_ui(order)
        result['ncf'] = order.ncf or None
        result['ncf_type'] = order.ncf_type or '02'
        result['ncf_expiration_date'] = order.ncf_expiration_date and order.ncf_expiration_date.strftime('%Y-%m-%d') or None
        _logger.info("[NCF] _export_for_ui - Orden: %s, NCF: %s, Tipo: %s", 
                     order.name, result['ncf'], result['ncf_type'])
        return result
