# -*- coding: utf-8 -*-
"""
Wizard para la selección y asignación de secuencias NCF a facturas.

Este módulo contiene el wizard transient que permite a los usuarios
seleccionar y asignar secuencias NCF a las facturas de manera interactiva.
"""

import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class NCFSequenceWizard(models.TransientModel):
    """Wizard para selección de secuencias NCF."""
    
    _name = 'ncf.sequence.wizard'
    _description = 'Wizard de Selección de NCF'
    _check_company_auto = True

    # Campos principales
    move_id = fields.Many2one(
        'account.move', 
        string='Factura',
        required=True,
        help="Factura a la que se asignará el NCF"
    )
    
    ncf_sequence_id = fields.Many2one(
        'ncf.sequence',
        string='Secuencia NCF',
        required=True,
        domain="[('active', '=', True), ('company_id', '=', company_id)]",
        help="Seleccione la secuencia NCF apropiada para esta factura"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company,
        help="Compañía de la factura"
    )
    
    ncf_type = fields.Selection(
        related='ncf_sequence_id.ncf_type',
        string='Tipo NCF',
        readonly=True,
        help="Tipo de NCF de la secuencia seleccionada"
    )
    
    current_ncf = fields.Char(
        string='NCF Actual',
        readonly=True,
        help="NCF actualmente asignado a la factura (si existe)"
    )

    @api.model
    def default_get(self, fields_list):
        """Establecer valores por defecto basados en el contexto."""
        res = super().default_get(fields_list)
        
        # Obtener la factura del contexto
        move_id = self.env.context.get('active_id')
        if move_id:
            move = self.env['account.move'].browse(move_id)
            res.update({
                'move_id': move_id,
                'company_id': move.company_id.id,
                'current_ncf': move.ncf or '',
            })
            
            # Si ya tiene una secuencia asignada, preseleccionarla
            if move.ncf_sequence_id:
                res['ncf_sequence_id'] = move.ncf_sequence_id.id
                
        return res

    @api.constrains('ncf_sequence_id', 'move_id')
    def _check_sequence_company(self):
        """Validar que la secuencia pertenezca a la misma compañía que la factura."""
        for wizard in self:
            if wizard.ncf_sequence_id.company_id != wizard.move_id.company_id:
                raise ValidationError(_(
                    "La secuencia NCF debe pertenecer a la misma compañía que la factura."
                ))

    def action_apply(self):
        """Aplicar la secuencia NCF seleccionada a la factura.
        
        Returns:
            dict: Acción para cerrar el wizard
            
        Raises:
            UserError: Si hay errores en la validación o asignación
        """
        self.ensure_one()
        
        try:
            # Validaciones previas
            if not self.move_id:
                raise UserError(_("No se ha especificado una factura."))
                
            if self.move_id.state != 'draft':
                raise UserError(_("Solo se puede asignar NCF a facturas en borrador."))
                
            if not self.ncf_sequence_id:
                raise UserError(_("Debe seleccionar una secuencia NCF."))

            # Generar el próximo NCF
            next_ncf = self.ncf_sequence_id._next()
            
            # Actualizar la factura
            vals = {
                'use_ncf': True,
                'ncf_sequence_id': self.ncf_sequence_id.id,
                'ncf': next_ncf,
                'ncf_type': self.ncf_sequence_id.ncf_type,
            }
            
            self.move_id.write(vals)
            
            _logger.info(
                "NCF %s assigned to invoice %s using sequence %s",
                next_ncf, self.move_id.name, self.ncf_sequence_id.name
            )
            
            return {
                'type': 'ir.actions.act_window_close',
                'infos': [_("NCF %s asignado correctamente.") % next_ncf]
            }
            
        except Exception as e:
            _logger.error("Error al asignar NCF: %s", str(e))
            raise UserError(_("Error al asignar NCF: %s") % str(e))

    def action_remove_ncf(self):
        """Remover el NCF de la factura.
        
        Returns:
            dict: Acción para cerrar el wizard
            
        Raises:
            UserError: Si la factura no está en borrador
        """
        self.ensure_one()
        
        if self.move_id.state != 'draft':
            raise UserError(_("Solo se puede remover NCF de facturas en borrador."))
            
        self.move_id.write({
            'use_ncf': False,
            'ncf_sequence_id': False,
            'ncf': False,
            'ncf_type': False,
        })
        
        _logger.info("NCF removed from invoice %s", self.move_id.name)
        
        return {
            'type': 'ir.actions.act_window_close',
            'infos': [_("NCF removido correctamente.")]
        }
