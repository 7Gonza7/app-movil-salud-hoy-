import os

# Extiende la ruta de búsqueda del paquete 'app' para incluir 'salud-hoy/app'
_repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_inner_app_dir = os.path.join(_repo_root, "salud-hoy", "app")

# Hacer que este paquete exponga los submódulos que están en 'salud-hoy/app'
__path__ = [p for p in (__path__ if '__path__' in globals() else [])] + [_inner_app_dir]



