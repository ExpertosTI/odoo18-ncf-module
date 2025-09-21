from odoo import models, fields, api, _
from odoo.exceptions import UserError

class AccountMove(models.Model):
    _inherit = 'account.move'

    ncf = fields.Char(string='Número de Comprobante Fiscal', readonly=True)
    use_ncf = fields.Boolean(string='Usar NCF', default=True)
    ncf_fiscal_type_id = fields.Many2one(
        'ncf.fiscal.type',
        string='Tipo de Comprobante',
        help='Tipo de comprobante fiscal NCF'
    )

    @api.onchange('use_ncf')
    def _onchange_use_ncf(self):
        """Handle NCF usage change - auto-select fiscal type if only one exists"""
        if self.use_ncf:
            fiscal_types = self.env['ncf.fiscal.type'].search([('active', '=', True)])
            if len(fiscal_types) == 1:
                self.ncf_fiscal_type_id = fiscal_types[0]
        else:
            self.ncf_fiscal_type_id = False

    def action_post(self):
        for move in self:
            if move.move_type == 'out_invoice' and move.use_ncf:
                if not move.ncf_fiscal_type_id:
                    # Try auto-selection one more time
                    fiscal_types = self.env['ncf.fiscal.type'].search([('active', '=', True)])
                    if len(fiscal_types) == 1:
                        move.ncf_fiscal_type_id = fiscal_types[0]
                    else:
                        raise UserError(_("Debe seleccionar un tipo de comprobante fiscal antes de confirmar la factura."))
                
                # Generate NCF using the selected fiscal type's sequence
                if move.ncf_fiscal_type_id and move.ncf_fiscal_type_id.sequence_id:
                    # Use the standard Odoo sequence
                    move.ncf = move.ncf_fiscal_type_id.sequence_id._next()
                else:
                    raise UserError(_("El tipo de comprobante seleccionado no tiene una secuencia configurada."))
        return super(AccountMove, self).action_post()

    def toggle_use_ncf(self):
        """Toggle NCF usage"""
        for move in self:
            move.use_ncf = not move.use_ncf

    def action_set_ncf_type(self):
        """Action to set NCF type with improved user experience"""
        self.ensure_one()
        fiscal_types = self.env['ncf.fiscal.type'].search([('active', '=', True)])
        
        if len(fiscal_types) == 0:
            raise UserError(_("No hay tipos de comprobante fiscal configurados. Configure al menos un tipo en el menú de Contabilidad."))
        elif len(fiscal_types) == 1:
            self.ncf_fiscal_type_id = fiscal_types[0]
            self.use_ncf = True
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('✅ NCF Configurado'),
                    'message': _('Tipo de comprobante seleccionado: %s') % fiscal_types[0].name,
                    'type': 'success',
                }
            }
        else:
            # Enable NCF and show selection dialog
            self.use_ncf = True
            return {
                'name': _('Seleccionar Tipo de Comprobante'),
                'type': 'ir.actions.act_window',
                'res_model': 'ncf.fiscal.type',
                'view_mode': 'tree',
                'target': 'new',
                'domain': [('active', '=', True)],
                'context': {
                    'default_active': True,
                    'search_default_active': True,
                }
            }