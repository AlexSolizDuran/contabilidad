# Contabilidad - API Django

Proyecto Django para gestión contable con DRF.

## Requisitos
- Python 3.11+
- pip
- (Opcional) virtualenv

## Configuración rápida (Windows PowerShell)
```powershell
# Clonar el repo
# git clone <URL_DEL_REPO>
# cd django

# Crear y activar entorno virtual (opcional)
python -m venv venv
./venv/Scripts/Activate.ps1

# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno (opcional usando .env)
# Crear archivo .env en la raíz con, por ejemplo:
# DEBUG=True
# SECRET_KEY= cambia_esta_clave
# ALLOWED_HOSTS=localhost,127.0.0.1

# Migraciones
python manage.py migrate

# Crear superusuario (opcional)
python manage.py createsuperuser

# Ejecutar servidor
python manage.py runserver
```

## Estructura
- `contabilidad/`: configuración del proyecto Django
- `gestion_cuentas/`, `gestion_asientos/`: apps con modelos, vistas y serializers

## Endpoints
Revisar `contabilidad/urls.py` y las `urls.py` de cada app para las rutas disponibles.

## Tests
```powershell
python manage.py test
```

## Despliegue
- Configura `ALLOWED_HOSTS`, `DEBUG=False` y una `SECRET_KEY` segura.
- Ejecuta migraciones en el servidor y configura `collectstatic` si usas archivos estáticos.
