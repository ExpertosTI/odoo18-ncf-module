from odoo import models, fields, api

class NCFSequence(models.Model):
    _name = 'ncf.sequence'
    _description = 'Secuencia NCF'

    name = fields.Char(string='Nombre', required=True, default="Secuencia NCF")
    prefix = fields.Char(string='Prefijo', required=True)
    padding = fields.Integer(string='Padding', default=8)
    number_next_actual = fields.Integer(string='Próximo Número', required=True, default=1)

    def _next(self):
        self.number_next_actual += 1
        return f"{self.prefix}{str(self.number_next_actual - 1).zfill(self.padding)}"