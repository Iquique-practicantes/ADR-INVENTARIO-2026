#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test de Cloudinary con nuevas credenciales"""
import cloudinary
import cloudinary.uploader
import cloudinary.api

# Nuevas credenciales
cloudinary.config(
    cloud_name="du16zsczw",
    api_key="667351511756756",
    api_secret="JTar5HkHWh49BK7e-aDJWx-sLIY",
    secure=True
)

print("Configuracion:")
print(f"  cloud_name: {cloudinary.config().cloud_name}")
print(f"  api_key: {cloudinary.config().api_key}")

print("\nProbando ping...")
try:
    result = cloudinary.api.ping()
    print(f"[OK] Conexion exitosa: {result}")
except Exception as e:
    print(f"[ERROR] {e}")

print("\nProbando subida...")
try:
    from io import BytesIO
    from PIL import Image
    
    img = Image.new('RGB', (100, 100), color='blue')
    buf = BytesIO()
    img.save(buf, 'JPEG')
    buf.seek(0)
    
    result = cloudinary.uploader.upload(buf, folder="test", public_id="test_img")
    print(f"[OK] Subida exitosa!")
    print(f"    URL: {result.get('secure_url')}")
    
    # Limpiar
    cloudinary.uploader.destroy(result['public_id'])
    print("[OK] Imagen de prueba eliminada")
except Exception as e:
    print(f"[ERROR] {e}")
