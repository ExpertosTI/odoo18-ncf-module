# -*- coding: utf-8 -*-
"""
Configuración global del módulo NCF.

Este módulo extiende la configuración de Odoo para permitir
la configuración de parámetros globales del sistema NCF.
"""

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    """Configuración de parámetros NCF en ajustes de contabilidad."""
    
    _inherit = 'res.config.settings'

    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF por Defecto',
        related='company_id.ncf_sequence_id',
        readonly=False,
        domain="[('active', '=', True), ('company_id', '=', company_id)]",
        help='Secuencia NCF que se usará por defecto para nuevas facturas'
    )
    
    ncf_control = fields.Boolean(
        string='Activar Control de NCF',
        related='company_id.ncf_control',
        readonly=False,
        help='Habilitar el control y validación de NCF en facturas'
    )
