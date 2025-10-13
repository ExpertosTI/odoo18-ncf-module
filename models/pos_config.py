# -*- coding: utf-8 -*-

from odoo import models, fields

class PosConfig(models.Model):
    _inherit = 'pos.config'
    
    enable_ncf = fields.Boolean(
        string='Habilitar NCF',
        default=True
    )
    
    default_ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF por Defecto',
        domain="[('company_id', '=', company_id), ('active', '=', True), ('ncf_type', '=', '02')]"
    )
    
    customer_details = fields.Boolean(
        string="Mostrar Datos Cliente",
        default=True
    )
    
    customer_name = fields.Boolean(
        string="Nombre Cliente",
        default=True
    )
    
    customer_vat = fields.Boolean(
        string="RNC/Cédula",
        default=True
    )
    
    customer_phone = fields.Boolean(
        string="Teléfono",
        default=True
    )
