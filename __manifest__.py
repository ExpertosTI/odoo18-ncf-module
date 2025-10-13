{
    'name': 'Número de Comprobante Fiscal RD - RENACE',
    'version': '18.0.1.2.1',
    'category': 'Accounting/Localizations',
    'summary': 'Genera Número de Comprobante Fiscal para República Dominicana - Proyecto RENACE',
    'description': """
        Módulo de Número de Comprobante Fiscal (NCF) para República Dominicana
        =====================================================================
        
        Gestión completa de secuencias NCF según regulaciones fiscales dominicanas.
        
        Características principales:
        * Gestión de secuencias NCF por tipo de comprobante
        * Integración con facturas de venta y notas de crédito
        * Integración completa con Punto de Venta (POS)
        * Botón selector de tipo de comprobante en POS
        * Impresión de NCF en tickets del POS
        * Wizard interactivo para selección de secuencias
        * Reportes fiscales especializados
        * Configuración por cliente y compañía
        * Multi-compañía con seguridad robusta
        
        Compatibilidad: Odoo 18.0+
    """,
    'author': 'Adderly Marte',
    'maintainer': 'Adderly Marte',
    'website': 'https://renace.tech',
    'license': 'LGPL-3',
    'depends': ['account', 'sale_management', 'point_of_sale'],
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
        'views/pos_config_views.xml',
        
        # Wizards
        'wizards/ncf_sequence_wizard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'ncf/static/src/css/ncf_styles.css',
        ],
        'point_of_sale._assets_pos': [
            'ncf/static/src/css/ncf_popup.css',
            'ncf/static/src/xml/order_receipt.xml',
            'ncf/static/src/xml/ncf_selection_popup.xml',
            'ncf/static/src/js/models.js',
            'ncf/static/src/js/pos_store.js',
            'ncf/static/src/js/control_buttons.js',
            'ncf/static/src/xml/control_buttons.xml',
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