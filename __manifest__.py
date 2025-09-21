{
    'name': 'Número de Comprobante Fiscal RD - RENACE',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Localizations',
    'summary': 'Genera Número de Comprobante Fiscal para República Dominicana - Proyecto RENACE',
    'description': """
        Módulo de Número de Comprobante Fiscal (NCF) para República Dominicana
        =====================================================================
        
        Este módulo permite la gestión de secuencias NCF según las regulaciones
        fiscales de República Dominicana (DGII) para el proyecto RENACE.
        
        🚀 VERSIÓN DE PRODUCCIÓN - ODOO 18.0
        
        Características principales:
        * ✅ Gestión completa de secuencias NCF por tipo de comprobante
        * ✅ Integración nativa con facturas de venta y notas de crédito
        * ✅ Wizard interactivo para selección de secuencias
        * ✅ Templates de factura optimizados para Odoo 18
        * ✅ Reportes fiscales especializados según DGII
        * ✅ Configuración granular por cliente y compañía
        * ✅ Seguridad multi-compañía robusta
        * ✅ Validaciones de integridad de datos
        * ✅ Logging completo para auditoría
        
        Migración y Compatibilidad:
        * Completamente reescrito para Odoo 18
        * Utiliza layout_document_title (nueva estructura QWeb)
        * Compatible con Community y Enterprise Edition
        * Soporte para Python 3.10+
        
        Desarrollado por RENACE - https://renace.tech
        Soporte técnico: info@renace.tech
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