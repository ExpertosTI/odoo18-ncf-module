# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'Account Move NCF'

    use_ncf = fields.Boolean('Usar NCF', default=False)
    ncf = fields.Char('NCF')
    ncf_sequence_id = fields.Many2one('ncf.sequence', string='Tipo de NCF')
    ncf_type = fields.Selection([
        ('01', 'Crédito Fiscal'),
        ('02', 'Consumo'),
        ('03', 'Nota Débito'),
        ('04', 'Nota Crédito'),
        ('11', 'Gubernamental'),
        ('12', 'Especial'),
        ('14', 'Regímenes Especiales'),
        ('15', 'Gubernamental Especial')
    ], string='Tipo de NCF', default='02')
    origin_ncf = fields.Char('NCF Original')

    def _post(self, soft=True):
        for move in self:
            if move.move_type == 'out_invoice' and move.use_ncf:
                if not move.ncf:
                    sequence = self.env['ncf.sequence'].search([], limit=1)
                    if not sequence:
                        raise UserError(_("No se ha configurado una secuencia NCF."))
                    move.ncf = sequence._next()
                move.payment_reference = move.ncf
        return super()._post(soft=soft)

    def toggle_use_ncf(self):
        self.ensure_one()
        if not self.use_ncf:
            action = {
                'name': _('Seleccionar Tipo de NCF'),
                'type': 'ir.actions.act_window',
                'res_model': 'ncf.sequence.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {'default_move_id': self.id}
            }
            return action
        else:
            self.use_ncf = False
            self.ncf = False
            self.ncf_sequence_id = False

    @api.model
    def create(self, vals):
        """
        Al crear la factura, si se marca usar NCF en borrador,
        asignamos el NCF y la referencia de pago.
        """
        move = super(AccountMove, self).create(vals)
        if move.use_ncf and move.ncf_sequence_id and not move.ncf:
            move.ncf = move.ncf_sequence_id._next()
        # Si tiene partner y no tiene secuencia NCF definida, usar la del partner
        if move.partner_id and move.move_type == 'out_invoice' and not move.ncf_sequence_id:
            if move.partner_id.default_ncf_sequence_id:
                move.write({
                    'use_ncf': True,
                    'ncf_sequence_id': move.partner_id.default_ncf_sequence_id.id
                })
                if not move.ncf:
                    move.ncf = move.ncf_sequence_id._next()
        return move

    def _print_invoice_auto(self):
        """
        Devuelve la acción del reporte de factura nativo (PDF) 
        para que se imprima automáticamente.
        """
        return self.env.ref('account.account_invoices').report_action(self)
