# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    default_ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Tipo de NCF por Defecto',
        help='Tipo de NCF que se usará por defecto en las facturas de este cliente'
    )
