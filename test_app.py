#!/usr/bin/env python3
"""
Script para validar la estructura de la aplicación CSF RD
sin necesidad de instalar Frappe localmente
"""

import os
import json
import sys
from pathlib import Path

def validate_app_structure():
    """Validar la estructura básica de la aplicación"""
    print("🔍 Validando estructura de la aplicación CSF RD...")
    
    # Verificar archivos esenciales
    essential_files = [
        "csf_rd/csf_rd/__init__.py",
        "csf_rd/csf_rd/hooks.py", 
        "csf_rd/csf_rd/modules.txt",
        "csf_rd/csf_rd/patches.txt",
        "setup.py",
        "requirements.txt"
    ]
    
    missing_files = []
    for file_path in essential_files:
        if not os.path.exists(file_path):
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ Todos los archivos esenciales están presentes")
    
    return True

def validate_hooks():
    """Validar configuración de hooks.py"""
    print("\n🔍 Validando hooks.py...")
    
    try:
        with open("csf_rd/csf_rd/hooks.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verificar elementos clave
        checks = [
            ("app_name", "csf_rd"),
            ("required_apps", "erpnext"),
            ("doctype_js", "DocType JavaScript overrides"),
            ("doc_events", "Document events"),
            ("jinja", "Jinja methods")
        ]
        
        for check, description in checks:
            if check in content:
                print(f"✅ {description}: OK")
            else:
                print(f"❌ {description}: FALTANTE")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo hooks.py: {e}")
        return False

def validate_doctypes():
    """Validar estructura de DocTypes"""
    print("\n🔍 Validando DocTypes...")
    
    doctype_dir = Path("csf_rd/csf_rd/doctype")
    if not doctype_dir.exists():
        print("❌ Directorio de DocTypes no encontrado")
        return False
    
    doctypes = ["dgii_customer", "dgii_settings", "ecf_document", "ncf_configuration"]
    
    for doctype in doctypes:
        doctype_path = doctype_dir / doctype
        if not doctype_path.exists():
            print(f"❌ DocType {doctype} no encontrado")
            return False
        
        # Verificar archivos del DocType
        required_files = [f"{doctype}.json", f"{doctype}.py", "__init__.py"]
        for file in required_files:
            if not (doctype_path / file).exists():
                print(f"❌ Archivo {file} faltante en {doctype}")
                return False
        
        # Validar JSON del DocType
        try:
            with open(doctype_path / f"{doctype}.json", "r") as f:
                doctype_data = json.load(f)
            
            required_fields = ["doctype", "name", "fields"]
            for field in required_fields:
                if field not in doctype_data:
                    print(f"❌ Campo {field} faltante en {doctype}.json")
                    return False
                    
        except json.JSONDecodeError as e:
            print(f"❌ JSON inválido en {doctype}.json: {e}")
            return False
    
    print("✅ Todos los DocTypes están correctamente estructurados")
    return True

def validate_reports():
    """Validar estructura de reportes"""
    print("\n🔍 Validando reportes...")
    
    report_dir = Path("csf_rd/csf_rd/report")
    if not report_dir.exists():
        print("❌ Directorio de reportes no encontrado")
        return False
    
    reports = ["dgii_tax_report", "ecf_summary_report"]
    
    for report in reports:
        report_path = report_dir / report
        if not report_path.exists():
            print(f"❌ Reporte {report} no encontrado")
            return False
        
        # Verificar archivos del reporte
        required_files = [f"{report}.json", f"{report}.py"]
        for file in required_files:
            if not (report_path / file).exists():
                print(f"❌ Archivo {file} faltante en {report}")
                return False
    
    print("✅ Todos los reportes están correctamente estructurados")
    return True

def validate_requirements():
    """Validar requirements.txt"""
    print("\n🔍 Validando requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            requirements = f.read().strip().split("\n")
        
        # Verificar que no incluye frappe/erpnext
        forbidden = ["frappe", "erpnext"]
        for req in requirements:
            if any(f in req.lower() for f in forbidden):
                print(f"❌ No debe incluir {req} en requirements.txt")
                return False
        
        print("✅ requirements.txt configurado correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo requirements.txt: {e}")
        return False

def main():
    """Función principal de validación"""
    print("🚀 Iniciando validación de la aplicación CSF RD...")
    print("=" * 50)
    
    validations = [
        validate_app_structure,
        validate_hooks,
        validate_doctypes,
        validate_reports,
        validate_requirements
    ]
    
    all_passed = True
    for validation in validations:
        if not validation():
            all_passed = False
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ¡TODAS LAS VALIDACIONES PASARON!")
        print("✅ Tu aplicación está lista para instalar en Frappe/ERPNext")
    else:
        print("❌ Algunas validaciones fallaron")
        print("🔧 Revisa los errores arriba y corrígelos")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
