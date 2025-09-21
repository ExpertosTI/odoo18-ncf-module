# -*- coding: utf-8 -*-

from odoo import models, fields


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF',
        config_parameter='l10n_do_ncf.default_sequence'
    )
    ncf_control = fields.Boolean('Control de NCF', default=True)
