# Módulo NCF (Número de Comprobante Fiscal) para Odoo 18

## Descripción

El módulo NCF proporciona funcionalidad completa para la gestión de Números de Comprobante Fiscal (NCF) en facturas de Odoo, cumpliendo con las regulaciones fiscales dominicanas y las mejores prácticas de Odoo 18.

### Características Principales

- ✅ **Gestión de Secuencias NCF**: Configuración y administración de diferentes tipos de secuencias NCF
- ✅ **Integración con Facturas**: Asignación automática y manual de NCF a facturas de venta y notas de crédito
- ✅ **Integración con POS**: Botón selector de tipo de comprobante en Punto de Venta
- ✅ **Ticket POS con NCF**: Impresión de NCF en tickets del POS
- ✅ **Wizard Interactivo**: Interfaz amigable para seleccionar y asignar secuencias NCF
- ✅ **Reportes Personalizados**: Templates de factura que muestran información NCF completa
- ✅ **Multi-Compañía**: Soporte completo para entornos multi-compañía con reglas de seguridad
- ✅ **Seguridad Granular**: Permisos y reglas de acceso por grupos de usuarios
- ✅ **Validaciones Robustas**: Controles de integridad y validaciones de datos
- ✅ **Logging Completo**: Registro detallado de operaciones para auditoría

## Instalación

### Requisitos Previos

- Odoo 18.0+
- Módulo `account` (Contabilidad) instalado
- Módulo `point_of_sale` (Punto de Venta) instalado
- Módulo `sale_management` (Ventas) instalado
- Permisos de administrador para instalar módulos

### Pasos de Instalación

1. Copiar el módulo `ncf` al directorio de addons de Odoo
2. Actualizar la lista de aplicaciones desde el menú de Apps
3. Buscar "NCF" e instalar el módulo
4. Configurar las secuencias NCF según sus necesidades

## Configuración

### 1. Configuración de Secuencias NCF

Navegue a **Contabilidad > Configuración > Secuencias NCF** para crear y configurar las secuencias:

```
Ejemplo de Configuración:
- Nombre: Factura de Consumo
- Prefijo: B01
- Padding: 8 dígitos
- Tipo NCF: 01 - Factura de Crédito Fiscal
- Compañía: Su compañía
```

### 2. Configuración Global

En **Contabilidad > Configuración > Ajustes**, configure la secuencia NCF por defecto.

### 3. Configuración de Clientes

En el formulario de clientes, puede asignar una secuencia NCF por defecto en la pestaña "Ventas y Compras".

### 4. Configuración de POS

En **Punto de Venta > Configuración > Punto de Venta**:
- Habilitar NCF en sección "Comprobantes Fiscales (NCF)"
- Seleccionar secuencia por defecto (recomendado: B02 - Factura de Consumo)

## Uso

### Asignación de NCF

1. **Manual**: Use los botones "Activar NCF" / "Desactivar NCF" en las facturas
2. **Automática**: Configure secuencias por defecto para asignación automática
3. **Wizard**: Use el wizard de selección para cambios avanzados

### Tipos de Documentos Soportados

- Facturas de venta (`out_invoice`)
- Notas de crédito (`out_refund`)
- Órdenes de Punto de Venta (`pos.order`)
- Soporte para diferentes tipos de NCF según regulaciones dominicanas

### Uso en Punto de Venta

1. Abrir sesión POS
2. Agregar productos a la orden
3. Click en botón NCF (muestra tipo actual, ej: "B02")
4. Seleccionar tipo de comprobante deseado
5. Procesar pago - el NCF se genera automáticamente
6. El ticket impreso muestra el NCF en dos ubicaciones

## Estructura del Módulo

```
ncf/
├── __manifest__.py              # Manifiesto con metadatos completos
├── models/
│   ├── account_move.py          # Extensión de facturas con NCF
│   ├── ncf_sequence.py          # Modelo principal de secuencias
│   ├── res_partner.py           # Extensión de clientes
│   ├── res_company.py           # Configuración por compañía
│   ├── res_config_settings.py   # Ajustes generales
│   ├── pos_config.py            # Configuración POS
│   ├── pos_order.py             # Órdenes POS con NCF
│   └── pos_session.py           # Carga datos NCF al POS
├── views/
│   ├── account_move_views.xml   # Vistas mejoradas de facturas
│   ├── account_move_template.xml # Template de reporte personalizado
│   ├── ncf_sequence_views.xml   # Vistas de configuración
│   ├── res_partner_views.xml    # Vistas de clientes
│   ├── res_config_settings_views.xml # Vistas de ajustes
│   ├── pos_config_views.xml     # Vistas configuración POS
│   └── report_fiscal_invoices.xml # Reportes fiscales
├── static/src/
│   ├── js/
│   │   ├── models.js            # Extensión Order con NCF
│   │   ├── pos_store.js         # Carga secuencias NCF
│   │   └── control_buttons.js   # Botón selector NCF
│   ├── xml/
│   │   ├── control_buttons.xml  # Template botón POS
│   │   └── order_receipt.xml    # Template ticket con NCF
│   └── css/
│       └── ncf_styles.css       # Estilos personalizados
├── wizards/
│   ├── ncf_sequence_wizard.py   # Wizard con validaciones robustas
│   └── ncf_sequence_wizard_views.xml # Interfaz del wizard
├── security/
│   ├── ir.model.access.csv      # Permisos granulares
│   └── ncf_security.xml         # Reglas multi-compañía
└── README.md                    # Esta documentación
```

## Mejores Prácticas Implementadas

### Código Python
- ✅ Documentación completa con docstrings
- ✅ Logging estructurado para auditoría
- ✅ Validaciones robustas con `@api.constrains`
- ✅ Manejo de errores con excepciones específicas
- ✅ Métodos auxiliares para reutilización de código
- ✅ Soporte multi-compañía con `_check_company_auto`

### Vistas XML
- ✅ Estructura XML bien formada con comentarios
- ✅ Uso de grupos de seguridad apropiados
- ✅ Campos con ayuda contextual (`help`)
- ✅ Dominios y contextos optimizados
- ✅ Vistas responsivas con clases Bootstrap

### Seguridad
- ✅ Access rights granulares por grupo de usuario
- ✅ Record rules para multi-compañía
- ✅ Grupos personalizados con herencia apropiada
- ✅ Validaciones de permisos en métodos críticos

### Manifest
- ✅ Metadatos completos según estándares Odoo 18
- ✅ Dependencias explícitas y organizadas
- ✅ Categorización apropiada
- ✅ Información de mantenimiento y soporte

## Seguridad y Permisos

### Grupos de Usuarios
- **NCF Administrator**: Acceso completo a configuración
- **Account Invoice**: Uso de NCF en facturas
- **Account User**: Gestión de secuencias
- **Account Manager**: Administración completa

### Reglas de Acceso
- Multi-compañía automática
- Filtrado por secuencias activas
- Permisos diferenciados por operación

## Solución de Problemas

### Problemas Comunes

1. **NCF no se genera**: Verificar secuencia activa y permisos
2. **Error multi-compañía**: Revisar configuración de compañías
3. **Secuencia agotada**: Ampliar rango o crear nueva secuencia

### Debugging

El módulo incluye logging detallado:
```python
_logger.info("NCF %s asignado a factura %s", ncf, invoice.name)
_logger.error("Error en validación NCF: %s", error)
```

## Desarrollo y Extensión

### Añadir Nuevos Tipos NCF

```python
# En models/ncf_sequence.py
NCF_TYPES = [
    ('01', 'Factura de Crédito Fiscal'),
    ('02', 'Factura de Consumo'),
    # Añadir nuevos tipos aquí
]
```

### Hooks Disponibles

- `_post()`: Generación automática al confirmar
- `create()`: Asignación en creación
- `write()`: Validaciones en modificación

## Testing y Calidad

### Validaciones Implementadas
- Formato de prefijo NCF
- Unicidad de números generados
- Consistencia multi-compañía
- Estados de documento válidos

### Verificación de Sintaxis
```bash
# XML
xmllint --noout ncf/views/*.xml

# Python
python3 -m py_compile ncf/models/*.py
```

## Licencia y Soporte

**Licencia**: LGPL-3  
**Desarrollado por**: Adderly Marte - RENACE  
**Sitio web**: https://renace.tech  
**Soporte**: info@renace.tech  

## Optimizaciones para Producción

### Rendimiento
- ✅ Índices de base de datos en campos críticos (ncf, prefix, ncf_type)
- ✅ SQL constraints para integridad de datos
- ✅ Búsquedas optimizadas con límites
- ✅ Operaciones batch donde sea posible
- ✅ Uso eficiente de sudo() solo cuando necesario

### Logging
- ✅ Niveles apropiados (INFO para producción, DEBUG removido)
- ✅ Formato consistente sin f-strings
- ✅ Traceback completo en errores (exc_info=True)
- ✅ Mensajes descriptivos en inglés para logs

### Seguridad
- ✅ check_company=True en campos relacionales
- ✅ copy=False en campos críticos (NCF, secuencias)
- ✅ Validaciones robustas con @api.constrains
- ✅ Permisos granulares por grupo de usuario
- ✅ Reglas multi-compañía automáticas

### Documentación
- ✅ Docstrings completos con formato Google Style
- ✅ Type hints en parámetros y retornos
- ✅ Ejemplos de uso en docstrings
- ✅ Comentarios en código complejo


## Changelog

### Versión 18.0.1.0.0 (Optimizada para Producción)
- ✅ Migración completa a Odoo 18
- ✅ Implementación de mejores prácticas oficiales Odoo
- ✅ Integración completa con Punto de Venta (POS)
- ✅ Botón selector de tipo de comprobante en POS
- ✅ Ticket POS con NCF impreso
- ✅ Seguridad multi-compañía robusta
- ✅ Wizard interactivo mejorado
- ✅ Validaciones robustas con constraints SQL y Python
- ✅ Logging optimizado para producción
- ✅ Índices de base de datos para performance
- ✅ Docstrings completos en todos los métodos
- ✅ Modelo res.company para configuración por compañía
- ✅ Optimización de consultas y búsquedas
- ✅ Manejo de errores robusto con trazabilidad completa

---

**Compatible con Odoo 18.0** | **Cumple regulaciones fiscales dominicanas** | **Listo para Producción** | **Mejores prácticas implementadas**