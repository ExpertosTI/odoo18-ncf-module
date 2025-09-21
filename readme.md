# Módulo NCF (Número de Comprobante Fiscal) para Odoo 18

[![Odoo Version](https://img.shields.io/badge/Odoo-18.0-blue.svg)](https://github.com/odoo/odoo/tree/18.0)
[![License](https://img.shields.io/badge/License-LGPL--3-green.svg)](https://www.gnu.org/licenses/lgpl-3.0.html)
[![Python Version](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)

## Descripción

El módulo NCF proporciona funcionalidad completa para la gestión de Números de Comprobante Fiscal (NCF) en facturas de Odoo, cumpliendo con las regulaciones fiscales dominicanas (DGII) y las mejores prácticas de Odoo 18.

**🚀 Versión de Producción - Odoo 18.0**

Este módulo ha sido específicamente desarrollado y optimizado para Odoo 18, incorporando las últimas mejoras en arquitectura de templates, QWeb y estructura de datos.

### Características Principales

- ✅ **Gestión de Secuencias NCF**: Configuración y administración de diferentes tipos de secuencias NCF
- ✅ **Integración con Facturas**: Asignación automática y manual de NCF a facturas de venta y notas de crédito
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

## Uso

### Asignación de NCF

1. **Manual**: Use los botones "Activar NCF" / "Desactivar NCF" en las facturas
2. **Automática**: Configure secuencias por defecto para asignación automática
3. **Wizard**: Use el wizard de selección para cambios avanzados

### Tipos de Documentos Soportados

- Facturas de venta (`out_invoice`)
- Notas de crédito (`out_refund`)
- Soporte para diferentes tipos de NCF según regulaciones dominicanas

## Estructura del Módulo

```
ncf/
├── __manifest__.py              # Manifiesto con metadatos completos
├── models/
│   ├── account_move.py          # Extensión de facturas con NCF
│   ├── ncf_sequence.py          # Modelo principal de secuencias
│   └── res_partner.py           # Extensión de clientes
├── views/
│   ├── account_move_views.xml   # Vistas mejoradas de facturas
│   ├── account_move_template.xml # Template de reporte personalizado
│   ├── ncf_sequence_views.xml   # Vistas de configuración
│   └── res_partner_views.xml    # Vistas de clientes
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

## Estructura del Proyecto

```
ncf/
├── __init__.py                 # Inicialización del módulo
├── __manifest__.py            # Manifiesto del módulo
├── models/                    # Modelos de datos
│   ├── account_move.py       # Extensión del modelo de facturas
│   ├── ncf_sequence.py       # Modelo de secuencias NCF
│   ├── res_config_settings.py # Configuraciones globales
│   └── res_partner.py        # Extensión de contactos
├── views/                     # Vistas y templates
│   ├── account_move_template.xml    # Template de factura NCF
│   ├── account_move_views.xml       # Vistas de facturas
│   ├── ncf_sequence_views.xml       # Vistas de secuencias
│   ├── report_fiscal_invoices.xml   # Reportes fiscales
│   ├── res_config_settings_views.xml # Vistas de configuración
│   └── res_partner_views.xml        # Vistas de contactos
├── wizards/                   # Asistentes
│   ├── ncf_sequence_wizard.py       # Lógica del wizard
│   └── ncf_sequence_wizard_views.xml # Vista del wizard
├── security/                  # Seguridad y permisos
│   ├── ir.model.access.csv          # Control de acceso
│   └── ncf_security.xml             # Reglas de seguridad
└── static/                    # Recursos estáticos
    └── description/
        ├── icon.png          # Icono del módulo
        └── index.html        # Descripción HTML
```

## Compatibilidad y Requisitos Técnicos

### Versiones Soportadas
- **Odoo**: 18.0 (Community y Enterprise)
- **Python**: 3.10+
- **PostgreSQL**: 12+

### Dependencias
- `base` - Módulo base de Odoo
- `account` - Módulo de contabilidad
- `web` - Framework web de Odoo

### Migración desde Versiones Anteriores
Este módulo ha sido completamente reescrito para Odoo 18. Si está migrando desde versiones anteriores:

1. **Backup completo** de su base de datos
2. **Desinstalar** versiones anteriores del módulo NCF
3. **Instalar** esta nueva versión
4. **Reconfigurar** las secuencias NCF según sus necesidades

## Contribución y Desarrollo

### Configuración del Entorno de Desarrollo
```bash
# Clonar el repositorio
git clone [URL_DEL_REPOSITORIO]

# Instalar en modo desarrollo
pip install -e .

# Ejecutar tests
python -m pytest tests/
```

### Estándares de Código
- **PEP 8** para Python
- **Odoo Guidelines** para estructura de módulos
- **XML Lint** para archivos de vista
- **Documentación** completa en código

## Licencia y Soporte

**Licencia**: LGPL-3  
**Desarrollado por**: Adderly Marte - RENACE  
**Sitio web**: https://renace.tech  
**Soporte**: info@renace.tech  

### Reportar Problemas
Para reportar bugs o solicitar nuevas funcionalidades, por favor:
1. Crear un issue en el repositorio
2. Incluir información detallada del problema
3. Proporcionar logs de error si aplica
4. Especificar versión de Odoo y del módulo

## Changelog

### Versión 18.0.1.0.0 (Actual)
- ✅ Migración completa a Odoo 18
- ✅ Implementación de mejores prácticas
- ✅ Seguridad multi-compañía
- ✅ Templates QWeb optimizados
- ✅ Corrección de XPath para layout_document_title
- ✅ Validaciones robustas de datos
- ✅ Logging completo de operaciones

---

**¿Necesitas ayuda?** Contacta con nuestro equipo de soporte técnico en info@renace.tech
- ✅ Wizard interactivo mejorado
- ✅ Documentación completa
- ✅ Validaciones robustas
- ✅ Logging estructurado

---

**Compatible con Odoo 18.0** | **Cumple regulaciones fiscales dominicanas** | **Mejores prácticas implementadas**