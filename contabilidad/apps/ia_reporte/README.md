# Sistema de IA para Generación de Reportes

Este módulo implementa un sistema de inteligencia artificial que permite generar reportes contables basados en solicitudes en lenguaje natural.

## Características

- **Interpretación de lenguaje natural**: Convierte solicitudes en texto a parámetros específicos de reportes
- **Generación automática de reportes**: Crea reportes basados en los datos del usuario y empresa
- **Múltiples tipos de reportes**: Balance General, Estado de Resultados, Libro Mayor, Libro Diario
- **Filtrado por empresa**: Solo muestra datos de la empresa del usuario autenticado

## Endpoints Disponibles

### 1. Generar Reporte con IA
```
POST /ia/generar-reporte/
```

**Parámetros:**
```json
{
    "texto_solicitud": "Genera un balance general al 31 de diciembre"
}
```

**Respuesta:**
```json
{
    "success": true,
    "solicitud_original": "Genera un balance general al 31 de diciembre",
    "interpretacion": {
        "tipo_reporte": "balance_general",
        "fecha_inicio": null,
        "fecha_fin": "2024-12-31",
        "cuentas_especificas": [],
        "clases_cuentas": [],
        "filtros_adicionales": {
            "estado_asientos": "APROBADO",
            "monto_minimo": null,
            "monto_maximo": null
        },
        "agrupacion": "por_cuenta",
        "ordenamiento": "ascendente",
        "descripcion_interpretada": "Balance general al 31 de diciembre"
    },
    "reporte": {
        "tipo": "balance_general",
        "fecha_corte": "2024-12-31",
        "activos": [...],
        "pasivos": [...],
        "patrimonio": [...]
    },
    "fecha_generacion": "2024-01-15T10:30:00Z",
    "empresa": "Mi Empresa S.A.S"
}
```

### 2. Obtener Ejemplos de Solicitudes
```
GET /ia/ejemplos/
```

### 3. Obtener Información de la Empresa
```
GET /ia/info-empresa/
```

## Tipos de Reportes Soportados

### Balance General
- **Solicitudes**: "balance general", "situación financiera", "estado de la empresa"
- **Datos**: Activos, Pasivos, Patrimonio agrupados por clases

### Estado de Resultados
- **Solicitudes**: "estado de resultados", "ganancias y pérdidas", "utilidad"
- **Datos**: Ingresos, Costos, Gastos, Utilidades

### Libro Mayor
- **Solicitudes**: "libro mayor", "mayor de cuenta", "saldo de cuentas"
- **Datos**: Movimientos detallados por cuenta

### Libro Diario
- **Solicitudes**: "libro diario", "asientos contables", "registro diario"
- **Datos**: Asientos ordenados cronológicamente

## Ejemplos de Solicitudes

### Balance General
- "Genera un balance general al 31 de diciembre"
- "Necesito el balance general de este año"
- "Muéstrame la situación financiera actual"

### Estado de Resultados
- "Genera el estado de resultados del último trimestre"
- "Necesito ver las ganancias y pérdidas de este año"
- "Muéstrame la utilidad del último mes"

### Libro Mayor
- "Genera el libro mayor de la cuenta 111 (Efectivo)"
- "Necesito el mayor de todas las cuentas de activos"
- "Muéstrame el mayor de las cuentas de gastos"

### Libro Diario
- "Genera el libro diario del último mes"
- "Necesito ver todos los asientos de este año"
- "Muéstrame los asientos del último trimestre"

## Configuración

### Variables de Entorno
```bash
OPENAI_API_KEY=tu_api_key_de_openai
```

### Instalación de Dependencias
```bash
pip install openai==1.54.4 langchain==0.3.7 langchain-openai==0.2.8
```

## Autenticación

Todos los endpoints requieren autenticación JWT. El sistema automáticamente:
- Identifica al usuario autenticado
- Obtiene la empresa asociada al usuario
- Filtra los datos solo de esa empresa

## Limitaciones

- Requiere API key de OpenAI
- Los reportes se generan basados en asientos aprobados
- Las fechas se interpretan en el contexto del año actual si no se especifican
- El sistema tiene un fallback básico si OpenAI no está disponible
