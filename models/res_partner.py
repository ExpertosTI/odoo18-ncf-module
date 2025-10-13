# -*- coding: utf-8 -*-
"""
Extensión del modelo res.partner para integración con NCF.

Este módulo extiende el modelo de contactos/clientes para permitir
la configuración de secuencias NCF por defecto.
"""

from odoo import models, fields


class ResPartner(models.Model):
    """Extensión de res.partner para configuración NCF por cliente."""
    
    _inherit = 'res.partner'

    default_ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Tipo de NCF por Defecto',
        company_dependent=True,
        check_company=True,
        domain="[('active', '=', True), ('company_id', 'in', [company_id, False])]",
        help='Tipo de NCF que se usará por defecto en las facturas de este cliente'
    )
