#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para ejecutar las pruebas del proyecto Salud Hoy
"""

import subprocess
import sys
import os

def run_tests():
    """Ejecuta todas las pruebas del proyecto"""
    print("=" * 70)
    print("  EJECUTANDO PRUEBAS - SALUD HOY")
    print("=" * 70)
    
    # Verificar que pytest esté instalado
    try:
        import pytest
        print("✓ pytest encontrado")
    except ImportError:
        print("✗ pytest no está instalado. Instalando...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pytest"])
        print("✓ pytest instalado")
    
    # Ejecutar las pruebas
    print("\n" + "=" * 70)
    print("  EJECUTANDO PRUEBAS...")
    print("=" * 70)
    
    try:
        # Ejecutar pytest con verbose
        result = subprocess.run([
            sys.executable, "-m", "pytest", 
            "tests/", 
            "-v", 
            "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        print("=" * 70)
        if result.returncode == 0:
            print("  TODAS LAS PRUEBAS PASARON ✓")
        else:
            print("  ALGUNAS PRUEBAS FALLARON ✗")
        print("=" * 70)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error ejecutando pruebas: {e}")
        return False

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)


