# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class NCFSequence(models.Model):
    _name = 'ncf.sequence'
    _description = 'Secuencia NCF'
    _order = 'name'
    _rec_name = 'name'

    name = fields.Char(
        string='Nombre',
        required=True,
        default="Secuencia NCF",
        tracking=True
    )
    prefix = fields.Char(
        string='Prefijo',
        required=True,
        tracking=True,
        help='Prefijo para el NCF (ej: B para facturas fiscales)'
    )
    padding = fields.Integer(
        string='Padding',
        default=8,
        tracking=True
    )
    number_next_actual = fields.Integer(
        string='Próximo Número',
        required=True,
        default=1,
        tracking=True
    )
    company_id = fields.Many2one(
        'res.company',
        required=True,
        default=lambda self: self.env.company
    )
    active = fields.Boolean(default=True)

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
    ], string='Tipo de NCF', required=True)

    _sql_constraints = [
        ('number_next_actual_positive', 'CHECK(number_next_actual > 0)', 'El próximo número debe ser mayor que 0'),
        ('prefix_unique', 'unique(prefix,company_id)', 'El prefijo debe ser único por compañía')
    ]

    @api.constrains('prefix')
    def _check_prefix(self):
        for record in self:
            if not record.prefix or len(record.prefix) < 1:
                raise UserError(_('El prefijo es requerido y debe tener al menos 1 carácter'))

    def _next(self):
        self.ensure_one()
        if not self.active:
            raise UserError(_('No se puede usar una secuencia inactiva'))
        current_str = str(self.number_next_actual).zfill(self.padding)
        self.sudo().number_next_actual += 1
        # Usar el prefijo configurado en lugar de hardcodear 'B'
        return f"{self.prefix}{self.ncf_type}{current_str}"

    def copy(self, default=None):
        default = dict(default or {})
        default.update(
            name=_("%s (copia)") % self.name,
            number_next_actual=1
        )
        return super().copy(default)
