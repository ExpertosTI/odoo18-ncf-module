# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class NCFSequenceWizard(models.TransientModel):
    _name = 'ncf.sequence.wizard'  # Simplificado
    _description = 'Wizard de Selección de NCF'

    move_id = fields.Many2one('account.move', string='Factura')
    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Tipo de NCF',
        required=True,
        domain="[('active', '=', True)]"
    )

    def action_apply(self):
        self.ensure_one()
        self.move_id.write({
            'use_ncf': True,
            'ncf_sequence_id': self.ncf_sequence_id.id,
            'ncf': self.ncf_sequence_id._next()
        })
        return {'type': 'ir.actions.act_window_close'}
