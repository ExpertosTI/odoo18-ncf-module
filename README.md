# 🇩🇴 Módulo NCF - Número de Comprobante Fiscal para República Dominicana

[![Odoo Version](https://img.shields.io/badge/Odoo-16.0-blue.svg)](https://github.com/odoo/odoo/tree/16.0)
[![License](https://img.shields.io/badge/License-LGPL--3-green.svg)](https://www.gnu.org/licenses/lgpl-3.0)
[![RENACE.TECH](https://img.shields.io/badge/Desarrollado%20por-RENACE.TECH-orange.svg)](https://renace.tech)

## 📋 Descripción

Módulo de localización para **República Dominicana** que implementa la generación automática de **Números de Comprobante Fiscal (NCF)** según las normativas de la **Dirección General de Impuestos Internos (DGII)**.

Este módulo permite a las empresas dominicanas cumplir con las regulaciones fiscales locales mediante la generación automática de NCF en facturas, notas de crédito, notas de débito y otros comprobantes fiscales.

## ✨ Características Principales

### 🎯 **Tipos de Comprobante Fiscal Soportados**
- **B01** - Factura de Crédito Fiscal
- **B02** - Factura de Consumo  
- **B03** - Nota de Débito
- **B04** - Nota de Crédito
- **B11** - Comprobante de Compras

### 🔧 **Funcionalidades**
- ✅ Generación automática de NCF en facturas
- ✅ Configuración de secuencias por tipo de comprobante
- ✅ Validación de formato según normativas DGII
- ✅ Integración completa con el módulo de contabilidad de Odoo
- ✅ Reportes fiscales personalizados
- ✅ Configuración flexible desde ajustes de la empresa

## 🚀 Instalación

### Prerrequisitos
- Odoo 16.0 o superior
- Módulo `account` (Contabilidad) instalado

### Pasos de Instalación

1. **Descargar el módulo**
   ```bash
   git clone https://github.com/ExpertosTI/odoo18-ncf-module.git
   cd odoo18-ncf-module
   git checkout 16.0
   ```

2. **Copiar a la carpeta de addons**
   ```bash
   cp -r . /path/to/odoo/addons/l10n_do_ncf/
   ```

3. **Actualizar lista de módulos**
   - Ir a **Aplicaciones** → **Actualizar Lista de Aplicaciones**

4. **Instalar el módulo**
   - Buscar "NCF" o "República Dominicana"
   - Hacer clic en **Instalar**

## ⚙️ Configuración

### 1. Configuración Inicial

Ir a **Contabilidad** → **Configuración** → **Ajustes** → **Localización Dominicana**

### 2. Configurar Tipos de Comprobante

1. Navegar a **Contabilidad** → **Configuración** → **Tipos de Comprobante Fiscal**
2. Los tipos predefinidos se crean automáticamente:
   - Factura de Crédito Fiscal (B01)
   - Factura de Consumo (B02)
   - Nota de Débito (B03)
   - Nota de Crédito (B04)
   - Comprobante de Compras (B11)

### 3. Configurar Secuencias NCF

1. Ir a **Contabilidad** → **Configuración** → **Secuencias NCF**
2. Configurar las secuencias para cada tipo de comprobante
3. Establecer el rango de numeración autorizado por la DGII

## 📖 Uso del Módulo

### Generación Automática de NCF

1. **Crear una factura** desde **Contabilidad** → **Clientes** → **Facturas**
2. **Seleccionar el tipo de comprobante fiscal** apropiado
3. Al **confirmar la factura**, el NCF se genera automáticamente
4. El número aparece en el campo **NCF** de la factura

### Reportes Fiscales

- **Reporte de Facturas Fiscales**: Listado completo de comprobantes generados
- **Secuencias por Tipo**: Control de numeración por cada tipo de comprobante
- **Validación de Rangos**: Verificación de números autorizados por DGII

## 🏗️ Estructura del Módulo

```
l10n_do_ncf/
├── __init__.py
├── __manifest__.py
├── data/
│   └── fiscal_type_data.xml      # Tipos de comprobante predefinidos
├── models/
│   ├── account_move.py           # Extensión de facturas
│   ├── ncf_fiscal_type.py        # Modelo de tipos fiscales
│   ├── ncf_sequence.py           # Secuencias NCF
│   └── res_config_settings.py    # Configuración
├── reports/
│   └── invoice_report.xml        # Reportes personalizados
├── security/
│   └── ir.model.access.csv       # Permisos de acceso
└── views/
    ├── account_move_views.xml     # Vistas de facturas
    ├── ncf_fiscal_type_views.xml  # Vistas de tipos fiscales
    ├── ncf_sequence_views.xml     # Vistas de secuencias
    └── res_config_settings_views.xml # Vistas de configuración
```

## 🔒 Seguridad y Permisos

El módulo incluye grupos de seguridad para:
- **Usuarios NCF**: Pueden generar comprobantes fiscales
- **Administradores NCF**: Pueden configurar tipos y secuencias
- **Auditores**: Solo lectura de reportes fiscales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para contribuir:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📞 Soporte

- **Desarrollador**: Adderly Marte
- **Email**: adderlymarte@renace.tech
- **Website**: [RENACE.TECH](https://renace.tech)
- **Repositorio**: [GitHub](https://github.com/ExpertosTI/odoo18-ncf-module)

## 📄 Licencia

Este módulo está licenciado bajo [LGPL-3.0](https://www.gnu.org/licenses/lgpl-3.0).

## 🏛️ Cumplimiento Legal

Este módulo ha sido desarrollado siguiendo las normativas fiscales de la **República Dominicana** establecidas por la **DGII (Dirección General de Impuestos Internos)**.

---

**⚠️ Nota Importante**: Este módulo es una herramienta de apoyo para el cumplimiento fiscal. Se recomienda consultar con un contador o asesor fiscal para asegurar el cumplimiento completo de las regulaciones locales.

---

<div align="center">
  <strong>Desarrollado con ❤️ por <a href="https://renace.tech">RENACE.TECH</a></strong>
</div>