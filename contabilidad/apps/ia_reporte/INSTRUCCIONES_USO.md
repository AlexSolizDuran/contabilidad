# Instrucciones de Uso - Sistema de IA para Reportes

## 🚀 Configuración Inicial

### 1. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno
Crear un archivo `.env` en la raíz del proyecto:
```bash
OPENAI_API_KEY=tu_api_key_de_openai_aqui
```

### 3. Configurar la App en Django
La app ya está agregada en `settings.py`:
```python
INSTALLED_APPS = [
    # ... otras apps
    'contabilidad.apps.ia_reporte'
]
```

## 📡 Endpoints Disponibles

### Generar Reporte con IA
```http
POST /ia/generar-reporte/
Authorization: Bearer <jwt_token>
Content-Type: application/json

{
    "texto_solicitud": "Genera un balance general de este año"
}
```

### Obtener Ejemplos
```http
GET /ia/ejemplos/
Authorization: Bearer <jwt_token>
```

### Información de Empresa
```http
GET /ia/info-empresa/
Authorization: Bearer <jwt_token>
```

## 💡 Ejemplos de Uso

### Balance General
```json
{
    "texto_solicitud": "Necesito el balance general al 31 de diciembre de este año"
}
```

### Estado de Resultados
```json
{
    "texto_solicitud": "Muéstrame las ganancias y pérdidas del último trimestre"
}
```

### Libro Mayor
```json
{
    "texto_solicitud": "Genera el libro mayor de la cuenta de efectivo"
}
```

### Libro Diario
```json
{
    "texto_solicitud": "Necesito ver todos los asientos del último mes"
}
```

## 🔧 Comando de Prueba

Para probar el sistema sin frontend:

```bash
python manage.py test_ia_reporte --usuario-id <user_id> --solicitud "Genera un balance general"
```

## 📊 Tipos de Reportes Soportados

| Tipo | Descripción | Ejemplo de Solicitud |
|------|-------------|---------------------|
| Balance General | Activos, Pasivos, Patrimonio | "Balance general de este año" |
| Estado de Resultados | Ingresos, Costos, Utilidades | "Estado de resultados del trimestre" |
| Libro Mayor | Movimientos por cuenta | "Mayor de la cuenta 111" |
| Libro Diario | Asientos cronológicos | "Libro diario del mes" |

## 🎯 Características de la IA

### Interpretación Inteligente
- Reconoce fechas: "último mes", "este año", "trimestre"
- Identifica tipos de reportes por palabras clave
- Extrae cuentas específicas por código o nombre
- Aplica filtros automáticamente

### Filtrado por Empresa
- Solo muestra datos de la empresa del usuario autenticado
- Respeta permisos y relaciones usuario-empresa
- Filtra asientos por estado (APROBADO por defecto)

### Fallback sin IA
- Si OpenAI no está disponible, usa interpretación básica
- Mantiene funcionalidad esencial
- Proporciona mensajes de error claros

## ⚙️ Configuración Avanzada

### Variables de Entorno Adicionales
```bash
# Configuración de OpenAI
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_TEMPERATURE=0.1
OPENAI_MAX_TOKENS=1000

# Límites de reportes
IA_MAX_CUENTAS_REPORTE=50
IA_MAX_ASIENTOS_REPORTE=100
IA_CONTEXTO_EMPRESA_LIMIT=20
```

### Personalización de Prompts
Editar `services.py` en el método `_interpretar_solicitud()` para personalizar cómo la IA interpreta las solicitudes.

## 🐛 Solución de Problemas

### Error: "OpenAI no está configurado"
- Verificar que `OPENAI_API_KEY` esté en el archivo `.env`
- Reiniciar el servidor Django

### Error: "Usuario no está asociado a ninguna empresa"
- Verificar que el usuario tenga una relación `UserEmpresa`
- Crear la relación si es necesario

### Reportes vacíos
- Verificar que existan asientos aprobados en la empresa
- Comprobar que las fechas del reporte sean correctas
- Revisar que las cuentas estén activas

## 📈 Mejoras Futuras

- [ ] Soporte para más tipos de reportes
- [ ] Exportación a PDF/Excel
- [ ] Gráficos y visualizaciones
- [ ] Análisis predictivo
- [ ] Integración con más modelos de IA
