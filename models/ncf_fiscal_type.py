from odoo import models, fields, api


class NCFFiscalType(models.Model):
    _name = 'ncf.fiscal.type'
    _description = 'Tipo de Comprobante Fiscal NCF'
    _order = 'code'

    name = fields.Char(
        string='Nombre del Comprobante',
        required=True,
        help='Ejemplo: Factura de Crédito Fiscal, Factura de Consumo, etc.'
    )
    prefix = fields.Char(
        string='Prefijo NCF',
        required=True,
        size=3,
        help='Ejemplo: B01, B02, B04, etc.'
    )
    # Campos calculados automáticamente
    code = fields.Char(
        string='Código',
        compute='_compute_code',
        store=True,
        help='Código extraído automáticamente del prefijo'
    )
    sequence_id = fields.Many2one(
        'ir.sequence',
        string='Secuencia',
        compute='_compute_sequence',
        store=True,
        help='Secuencia generada automáticamente'
    )
    active = fields.Boolean(
        string='Activo',
        default=True,
        help='Si está marcado, este tipo de comprobante estará disponible para usar'
    )

    _sql_constraints = [
        ('prefix_unique', 'unique(prefix)', 'El prefijo del tipo de comprobante debe ser único.'),
    ]

    @api.depends('prefix')
    def _compute_code(self):
        """Extraer código automáticamente del prefijo"""
        for record in self:
            if record.prefix and len(record.prefix) >= 2:
                # Extraer los últimos 2 dígitos del prefijo (ej: B01 -> 01)
                record.code = record.prefix[-2:]
            else:
                record.code = False

    @api.depends('prefix', 'name')
    def _compute_sequence(self):
        """Crear secuencia automáticamente"""
        for record in self:
            if record.prefix and record.name:
                # Buscar si ya existe una secuencia
                existing_seq = self.env['ir.sequence'].search([
                    ('code', '=', f'ncf.{record.prefix.lower()}')
                ], limit=1)
                
                if existing_seq:
                    record.sequence_id = existing_seq
                else:
                    # Crear nueva secuencia
                    sequence_vals = {
                        'name': f'NCF {record.name}',
                        'code': f'ncf.{record.prefix.lower()}',
                        'prefix': f'{record.prefix}',
                        'suffix': '',
                        'padding': 8,
                        'number_next': 1,
                        'number_increment': 1,
                        'implementation': 'standard',
                    }
                    new_sequence = self.env['ir.sequence'].create(sequence_vals)
                    record.sequence_id = new_sequence
            else:
                record.sequence_id = False

    def name_get(self):
        """Personalizar la visualización del nombre"""
        result = []
        for record in self:
            name = f"{record.prefix} - {record.name}"
            result.append((record.id, name))
        return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100, name_get_uid=None):
        """Permitir búsqueda por código y prefijo además del nombre"""
        if args is None:
            args = []
        if name:
            domain = ['|', '|', ('name', operator, name), ('code', operator, name), ('prefix', operator, name)]
            args = domain + args
        return super()._name_search(name, args, operator, limit, name_get_uid)