# -*- coding: utf-8 -*-
"""
Módulo NCF Sequence para gestión de secuencias de Número de Comprobante Fiscal
en República Dominicana según regulaciones fiscales.
"""

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class NCFSequence(models.Model):
    """Modelo para gestionar secuencias de Número de Comprobante Fiscal (NCF)."""
    
    _name = 'ncf.sequence'
    _description = 'Secuencia NCF para República Dominicana'
    _order = 'name, company_id'
    _rec_name = 'name'
    _check_company_auto = True

    # Campos básicos
    name = fields.Char(
        string='Nombre',
        required=True,
        default="Secuencia NCF",
        tracking=True,
        translate=False,
        help="Nombre descriptivo de la secuencia NCF"
    )
    
    prefix = fields.Char(
        string='Prefijo',
        required=True,
        tracking=True,
        size=3,
        help='Prefijo para el NCF (ej: B para facturas fiscales)'
    )
    
    padding = fields.Integer(
        string='Padding',
        default=8,
        tracking=True,
        help="Número de dígitos para el número secuencial"
    )
    
    number_next_actual = fields.Integer(
        string='Próximo Número',
        required=True,
        default=1,
        tracking=True,
        help="Próximo número a utilizar en la secuencia"
    )
    
    company_id = fields.Many2one(
        'res.company',
        string='Compañía',
        required=True,
        default=lambda self: self.env.company,
        help="Compañía a la que pertenece esta secuencia"
    )
    
    active = fields.Boolean(
        string='Activo',
        default=True,
        help="Si está inactivo, no se puede usar esta secuencia"
    )

    ncf_type = fields.Selection([
        ('01', 'Factura de Crédito Fiscal'),
        ('02', 'Factura de Consumo'),
        ('03', 'Notas de Débito'),
        ('04', 'Notas de Crédito'),
        ('11', 'Comprobante de Compras'),
        ('12', 'Registro Único de Ingresos'),
        ('13', 'Comprobante para Gastos Menores'),
        ('14', 'Regímenes Especiales'),
        ('15', 'Comprobante Gubernamental'),
        ('16', 'Comprobante para Exportaciones'),
        ('17', 'Comprobante para Pagos al Exterior')
    ], 
    string='Tipo de NCF', 
    required=True,
    default='02',
    help="Tipo de comprobante fiscal según regulaciones dominicanas"
    )

    # Restricciones SQL
    _sql_constraints = [
        ('number_next_actual_positive', 
         'CHECK(number_next_actual > 0)', 
         'El próximo número debe ser mayor que 0'),
        ('ncf_type_company_unique', 
         'unique(ncf_type, company_id)', 
         'Ya existe una secuencia con este tipo de NCF para esta compañía. Solo puede haber una secuencia activa por tipo de NCF.'),
        ('padding_valid',
         'CHECK(padding >= 1 AND padding <= 20)',
         'El padding debe estar entre 1 y 20 dígitos')
    ]

    @api.constrains('ncf_type', 'company_id', 'active')
    def _check_unique_active_ncf_type(self):
        """Validar que solo haya una secuencia activa por tipo NCF + compañía.
        
        Según las regulaciones dominicanas, el prefijo 'B' es común para todos los tipos,
        por lo que la unicidad debe basarse en el tipo de NCF, no en el prefijo.
        """
        for record in self:
            if record.ncf_type and record.company_id and record.active:
                existing = self.search([
                    ('ncf_type', '=', record.ncf_type),
                    ('company_id', '=', record.company_id.id),
                    ('active', '=', True),
                    ('id', '!=', record.id)
                ])
                if existing:
                    raise ValidationError(_(
                        'Ya existe una secuencia NCF activa del tipo "%s" para la compañía "%s".\n'
                        'Solo puede haber una secuencia activa por tipo de NCF por compañía.\n\n'
                        'Secuencia existente: %s\n\n'
                        'Nota: El prefijo "B" es común para todos los tipos según regulaciones dominicanas.'
                    ) % (dict(record._fields['ncf_type'].selection)[record.ncf_type], 
                         record.company_id.name, existing[0].name))

    @api.constrains('prefix')
    def _check_prefix(self):
        """Validar que el prefijo tenga el formato correcto."""
        for record in self:
            if not record.prefix:
                raise ValidationError(_('El prefijo es requerido'))
            if len(record.prefix) < 1 or len(record.prefix) > 3:
                raise ValidationError(_('El prefijo debe tener entre 1 y 3 caracteres'))
            if not record.prefix.isalpha():
                raise ValidationError(_('El prefijo solo puede contener letras'))

    @api.constrains('padding')
    def _check_padding(self):
        """Validar que el padding esté en un rango válido."""
        for record in self:
            if record.padding < 1 or record.padding > 20:
                raise ValidationError(_('El padding debe estar entre 1 y 20 dígitos'))

    def _next(self):
        """
        Generar el próximo número NCF de la secuencia.
        
        Returns:
            str: Número NCF formateado
        """
        self.ensure_one()
        if not self.active:
            raise UserError(_('No se puede usar una secuencia inactiva'))
        
        # Validar que ncf_type esté definido
        if not self.ncf_type:
            raise UserError(_('La secuencia NCF debe tener un tipo definido'))
        
        try:
            current_str = str(self.number_next_actual).zfill(self.padding)
            self.sudo().number_next_actual += 1
            ncf_number = f"{self.prefix}{self.ncf_type}{current_str}"
            
            _logger.debug(f"NCF generado: {ncf_number} para secuencia {self.name}")
            return ncf_number
            
        except Exception as e:
            _logger.error(f"Error generando NCF: {e}")
            raise UserError(_('Error al generar el número NCF: %s') % str(e))

    @api.model
    def create(self, vals):
        """Override create para logging y validaciones adicionales."""
        result = super().create(vals)
        _logger.debug(f"Nueva secuencia NCF creada: {result.name}")
        return result

    def copy(self, default=None):
        """Override copy para manejar duplicación correctamente."""
        default = dict(default or {})
        default.update({
            'name': _("%s (copia)") % self.name,
            'number_next_actual': 1
        })
        return super().copy(default)

    def name_get(self):
        """Personalizar la representación del nombre."""
        result = []
        for record in self:
            name = f"{record.name} [{record.prefix}{record.ncf_type}]"
            result.append((record.id, name))
        return result
