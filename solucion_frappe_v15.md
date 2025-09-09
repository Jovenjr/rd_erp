# Solución para Problema de override_doctype_class en Frappe v15

## Problema Identificado
- DocTypes con `override_doctype_class` marcados como "orphaned" 
- Frappe busca controladores en `frappe.core.doctype` en lugar del módulo correcto
- Issue reportado: https://github.com/frappe/frappe/issues/23052

## Soluciones que han funcionado para otros desarrolladores:

### 1. Ejecutar `bench migrate` (Más efectiva)
```bash
bench --site [tu-sitio] migrate
```

### 2. Habilitar modo desarrollador
```bash
bench set-config developer_mode 1
bench clear-cache
bench restart
```

### 3. Verificar orden de aplicaciones en apps.txt
```bash
# Asegurar que csf_rd esté al final
bench --site [tu-sitio] list-apps
```

### 4. Reinstalar con migración
```bash
bench --site [tu-sitio] uninstall-app csf_rd
bench --site [tu-sitio] install-app csf_rd
bench migrate
bench restart
```

### 5. Verificar hooks después de migración
```python
# En consola de Frappe
import frappe
print(frappe.get_hooks("override_doctype_class"))
```

## Comandos de diagnóstico:
```bash
# Verificar aplicaciones instaladas
bench list-apps

# Verificar estado de migración
bench --site [tu-sitio] migrate --dry-run

# Limpiar caché
bench clear-cache

# Reiniciar servicios
bench restart
```
