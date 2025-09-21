{
    'name': 'NCF República Dominicana',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Genera Número de Comprobante Fiscal para República Dominicana - Proyecto RENACE',
    'author': 'Adderly Marte',
    'website': 'https://renace.tech',
    'license': 'LGPL-3',
    'support': 'adderlymarte@renace.tech',
    'depends': ['account', 'sale_management'],
    'data': [
        'security/ncf_security.xml',  # Seguridad base: registra el modelo del wizard
        'security/ir.model.access.csv',  # Luego se asignan los permisos
        'wizards/ncf_sequence_wizard_view.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/ncf_sequence_views.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_template.xml',
        'views/report_fiscal_invoices.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}