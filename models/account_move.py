# -*- coding: utf-8 -*-
"""
Extensión del modelo account.move para integración con NCF (Número de Comprobante Fiscal)
según regulaciones fiscales de República Dominicana.
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class AccountMove(models.Model):
    """Extensión de account.move para funcionalidad NCF."""
    
    _inherit = 'account.move'

    # SQL Constraints
    _sql_constraints = [
        ('ncf_unique', 
         'unique(ncf, company_id)', 
         'El NCF debe ser único por compañía. Este NCF ya existe en el sistema.'),
    ]

    # Campos NCF
    use_ncf = fields.Boolean(
        string='Usar NCF',
        default=False,
        help="Indica si esta factura debe usar Número de Comprobante Fiscal"
    )
    
    ncf = fields.Char(
        string='NCF',
        size=19,
        copy=False,
        index=True,
        help="Número de Comprobante Fiscal generado automáticamente"
    )
    
    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF',
        copy=False,
        check_company=True,
        help="Secuencia utilizada para generar el NCF"
    )
    
    ncf_expiration_date = fields.Date(
        string='Fecha Vencimiento NCF',
        copy=False,
        compute='_compute_ncf_expiration_date',
        store=True,
        help="Fecha de vencimiento del comprobante fiscal (30 días desde emisión)"
    )
    
    @api.depends('invoice_date', 'use_ncf')
    def _compute_ncf_expiration_date(self):
        from datetime import date
        for move in self:
            if move.use_ncf and move.invoice_date:
                year = move.invoice_date.year
                move.ncf_expiration_date = date(year, 12, 31)
            else:
                move.ncf_expiration_date = False
    
    ncf_type = fields.Selection([
        ('01', 'Crédito Fiscal'),
        ('02', 'Consumo'),
        ('03', 'Nota Débito'),
        ('04', 'Nota Crédito'),
        ('11', 'Gubernamental'),
        ('12', 'Especial'),
        ('14', 'Regímenes Especiales'),
        ('15', 'Gubernamental Especial')
    ], 
    string='Tipo de NCF', 
    default='02',
    help="Tipo de comprobante fiscal según regulaciones dominicanas"
    )
    
    origin_ncf = fields.Char(
        string='NCF Original',
        size=19,
        help="NCF original para notas de crédito/débito"
    )

    @api.constrains('ncf')
    def _check_ncf_format(self):
        """Validar formato del NCF."""
        for record in self:
            if record.ncf and len(record.ncf) > 19:
                raise ValidationError(_('El NCF no puede tener más de 19 caracteres'))

    def _post(self, soft=True):
        """Override _post para generar NCF automáticamente al confirmar factura.
        
        Args:
            soft (bool): Si True, permite post parcial en caso de errores
            
        Returns:
            bool: Resultado del post
            
        Raises:
            UserError: Si no hay secuencia NCF configurada o error al generar
        """
        for move in self:
            if move.move_type == 'out_invoice' and move.use_ncf and not move.ncf:
                if not move.ncf_sequence_id:
                    # Buscar secuencia por defecto desde la compañía
                    sequence = move.company_id.ncf_sequence_id
                    if not sequence:
                        # Fallback: buscar cualquier secuencia activa
                        sequence = self.env['ncf.sequence'].search([
                            ('company_id', '=', move.company_id.id),
                            ('active', '=', True)
                        ], limit=1)
                    if not sequence:
                        raise UserError(_("No se ha configurado una secuencia NCF activa para esta compañía."))
                    move.ncf_sequence_id = sequence
                
                try:
                    move.ncf = move.ncf_sequence_id._next()
                    move.payment_reference = move.ncf
                    _logger.info("NCF %s assigned to invoice %s", move.ncf, move.name)
                except Exception as e:
                    _logger.error("Error assigning NCF to invoice %s: %s", move.name, e, exc_info=True)
                    raise UserError(_('Error al generar NCF: %s') % str(e))
        
        return super()._post(soft=soft)

    def toggle_use_ncf(self):
        """Alternar el uso de NCF y abrir wizard de selección si es necesario."""
        self.ensure_one()
        
        if self.state != 'draft':
            raise UserError(_('Solo se puede modificar el NCF en facturas en borrador'))
        
        if not self.use_ncf:
            # Activar NCF - abrir wizard para seleccionar secuencia
            action = {
                'name': _('Seleccionar Tipo de NCF'),
                'type': 'ir.actions.act_window',
                'res_model': 'ncf.sequence.wizard',
                'view_mode': 'form',
                'target': 'new',
                'context': {
                    'default_move_id': self.id,
                    'default_company_id': self.company_id.id
                }
            }
            return action
        else:
            # Desactivar NCF - mostrar confirmación
            self.write({
                'use_ncf': False,
                'ncf': False,
                'ncf_sequence_id': False
            })
            _logger.info("NCF deactivated for invoice %s", self.name)
            
            # Retornar mensaje de éxito
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('NCF Desactivado'),
                    'message': _('El NCF ha sido desactivado correctamente para esta factura.'),
                    'type': 'success',
                    'sticky': False,
                }
            }

    @api.model_create_multi
    def create(self, vals_list):
        """Override create para manejar NCF en creación de facturas."""
        moves = super().create(vals_list)
        
        for move in moves:
            if (move.partner_id and 
                move.move_type == 'out_invoice' and 
                not move.ncf_sequence_id and
                hasattr(move.partner_id, 'default_ncf_sequence_id') and
                move.partner_id.default_ncf_sequence_id):
                
                move.write({
                    'use_ncf': True,
                    'ncf_sequence_id': move.partner_id.default_ncf_sequence_id.id
                })
                _logger.info("NCF sequence auto-assigned from partner for invoice %s", move.name)
        
        return moves

    def write(self, vals):
        """Override write para validaciones adicionales."""
        # Validar que no se modifique NCF en facturas confirmadas
        if 'ncf' in vals:
            for record in self:
                if record.state != 'draft' and record.ncf != vals.get('ncf'):
                    raise UserError(_('No se puede modificar el NCF de una factura confirmada'))
        
        return super().write(vals)

    def _print_invoice_auto(self):
        """
        Devuelve la acción del reporte de factura nativo (PDF) 
        para que se imprima automáticamente.
        """
        return self.env.ref('account.account_invoices').report_action(self)

    def action_view_ncf_sequence(self):
        """Acción para ver la secuencia NCF asociada."""
        self.ensure_one()
        if not self.ncf_sequence_id:
            raise UserError(_('Esta factura no tiene una secuencia NCF asociada'))
        
        return {
            'name': _('Secuencia NCF'),
            'type': 'ir.actions.act_window',
            'res_model': 'ncf.sequence',
            'res_id': self.ncf_sequence_id.id,
            'view_mode': 'form',
            'target': 'current',
        }
