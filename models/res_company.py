# -*- coding: utf-8 -*-
"""
Extensión del modelo res.company para integración con NCF.

Este módulo extiende el modelo de compañías para almacenar
configuraciones NCF a nivel de compañía.
"""

from odoo import models, fields


class ResCompany(models.Model):
    """Extensión de res.company para configuración NCF."""
    
    _inherit = 'res.company'

    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF por Defecto',
        domain="[('active', '=', True), ('company_id', '=', id)]",
        help='Secuencia NCF que se usará por defecto para nuevas facturas de esta compañía'
    )
    
    ncf_control = fields.Boolean(
        string='Activar Control de NCF',
        default=True,
        help='Habilitar el control y validación de NCF en facturas de esta compañía'
    )
