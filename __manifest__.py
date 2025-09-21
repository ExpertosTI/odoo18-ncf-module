{
    'name': 'NCF República Dominicana',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Genera Número de Comprobante Fiscal para República Dominicana - Proyecto RENACE',
    'description': """
Número de Comprobante Fiscal (NCF) - República Dominicana
==========================================================

Gestiona secuencias NCF según regulaciones DGII para facturas y notas de crédito.

Funcionalidades:
• Secuencias NCF automáticas por tipo de comprobante
• Integración con facturas de venta y notas de crédito  
• Wizard de selección de secuencias
• Reportes fiscales DGII
• Configuración por cliente y compañía
• Validaciones de integridad fiscal

Compatible con Odoo 18 Community y Enterprise.
    """,
    'author': 'Adderly Marte - RENACE',
    'maintainer': 'RENACE Tech Solutions',
    'website': 'https://renace.tech',
    'support': 'info@renace.tech',
    'license': 'LGPL-3',
    'depends': ['account', 'sale_management'],
    'external_dependencies': {
        'python': [],
    },
    'data': [
        # Security
        'security/ir.model.access.csv',
        'security/ncf_security.xml',
        
        # Views
        'views/ncf_sequence_views.xml',
        'views/res_config_settings_views.xml',
        'views/res_partner_views.xml',
        'views/account_move_views.xml',
        'views/account_move_template.xml',
        'views/report_fiscal_invoices.xml',
        
        # Wizards
        'wizards/ncf_sequence_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ncf/static/src/css/ncf_styles.css',
            'ncf/static/src/js/ncf_interactions.js',
        ],
    },
    'demo': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 0.0,
    'currency': 'USD',
}