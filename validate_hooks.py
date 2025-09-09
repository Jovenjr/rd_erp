#!/usr/bin/env python3
"""
Script para validar específicamente el hook override_doctype_class
"""

import os
import json
from pathlib import Path

def validate_override_doctype_class():
    """Validar configuración de override_doctype_class"""
    print("🔍 Validando override_doctype_class...")
    
    # Leer hooks.py
    try:
        with open("csf_rd/hooks.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Verificar que existe override_doctype_class
        if "override_doctype_class" not in content:
            print("❌ override_doctype_class no encontrado en hooks.py")
            return False
        
        print("✅ override_doctype_class encontrado en hooks.py")
        
        # Verificar que las clases existen
        classes_to_check = [
            "DGIICustomer",
            "DGIISettings", 
            "ECFDocument",
            "NCFConfiguration"
        ]
        
        for class_name in classes_to_check:
            if class_name in content:
                print(f"✅ Clase {class_name} referenciada en hooks.py")
            else:
                print(f"❌ Clase {class_name} NO encontrada en hooks.py")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Error leyendo hooks.py: {e}")
        return False

def validate_controller_files():
    """Validar que los archivos de controlador existen y tienen las clases correctas"""
    print("\n🔍 Validando archivos de controlador...")
    
    controllers = [
        ("csf_rd/doctype/dgii_customer/dgii_customer.py", "DGIICustomer"),
        ("csf_rd/doctype/dgii_settings/dgii_settings.py", "DGIISettings"),
        ("csf_rd/doctype/ecf_document/ecf_document.py", "ECFDocument"),
        ("csf_rd/doctype/ncf_configuration/ncf_configuration.py", "NCFConfiguration")
    ]
    
    for file_path, expected_class in controllers:
        if not os.path.exists(file_path):
            print(f"❌ Archivo {file_path} no encontrado")
            return False
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            if f"class {expected_class}(Document):" in content:
                print(f"✅ {file_path}: Clase {expected_class} encontrada")
            else:
                print(f"❌ {file_path}: Clase {expected_class} NO encontrada")
                return False
                
        except Exception as e:
            print(f"❌ Error leyendo {file_path}: {e}")
            return False
    
    return True

def validate_doctype_json():
    """Validar que los DocTypes JSON tienen la configuración correcta"""
    print("\n🔍 Validando configuración de DocTypes JSON...")
    
    doctypes = [
        "csf_rd/doctype/dgii_customer/dgii_customer.json",
        "csf_rd/doctype/dgii_settings/dgii_settings.json",
        "csf_rd/doctype/ecf_document/ecf_document.json",
        "csf_rd/doctype/ncf_configuration/ncf_configuration.json"
    ]
    
    for doctype_path in doctypes:
        try:
            with open(doctype_path, "r", encoding="utf-8") as f:
                doctype_data = json.load(f)
            
            # Verificar que es custom
            if doctype_data.get("custom", 0) == 1:
                print(f"✅ {doctype_path}: Marcado como custom")
            else:
                print(f"⚠️  {doctype_path}: No marcado como custom (puede ser correcto)")
            
            # Verificar módulo
            if doctype_data.get("module") == "csf_rd":
                print(f"✅ {doctype_path}: Módulo correcto (csf_rd)")
            else:
                print(f"❌ {doctype_path}: Módulo incorrecto ({doctype_data.get('module')})")
                return False
                
        except Exception as e:
            print(f"❌ Error leyendo {doctype_path}: {e}")
            return False
    
    return True

def main():
    """Función principal de validación"""
    print("🚀 Validando configuración de controladores personalizados...")
    print("=" * 60)
    
    validations = [
        validate_override_doctype_class,
        validate_controller_files,
        validate_doctype_json
    ]
    
    all_passed = True
    for validation in validations:
        if not validation():
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ¡TODAS LAS VALIDACIONES PASARON!")
        print("✅ Los controladores personalizados están configurados correctamente")
        print("✅ Frappe debería poder resolver los controladores correctamente")
    else:
        print("❌ Algunas validaciones fallaron")
        print("🔧 Revisa los errores arriba y corrígelos")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
