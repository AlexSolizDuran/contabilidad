import os
import json
from datetime import datetime
# Carpeta raíz para los logs
LOG_DIR = "logs"

def registrar_evento(id_sesion, datos_usuario, nivel, accion, detalle, fin_sesion=False):
    """
    Registra un evento en el archivo JSON del usuario correspondiente (por día).
    Crea carpetas por empresa y por usuario, y guarda los logs agrupados por fecha.
    """
    # Fecha y hora actuales
    ahora = datetime.utcnow().isoformat() + "Z"
    fecha_actual = datetime.utcnow().strftime("%Y-%m-%d")

    empresa_id = datos_usuario.get("empresa", "empresa_desconocida")
    usuario_id = datos_usuario.get("usuario", "desconocido")

    # Carpeta por empresa (logs/empresa_x/)
    carpeta_empresa = os.path.join(LOG_DIR, empresa_id)
    os.makedirs(carpeta_empresa, exist_ok=True)

    # Carpeta por usuario dentro de la empresa (logs/empresa_x/usuario_y/)
    carpeta_usuario = os.path.join(carpeta_empresa, usuario_id)
    os.makedirs(carpeta_usuario, exist_ok=True)


    # Archivo del día (logs/empresa_x/usuario_y/2025-10-15.json)
    archivo = os.path.join(carpeta_usuario, f"{fecha_actual}.json")

    # Cargar logs previos del día si existen
    if os.path.exists(archivo):
        with open(archivo, "r", encoding="utf-8") as f:
            logs_dia = json.load(f)
    else:
        logs_dia = []

    # Buscar si ya existe un log para esta sesión
    log_sesion = next((log for log in logs_dia if log["idSesion"] == id_sesion), None)

    if not log_sesion:
        # Crear estructura nueva de sesión
        log_sesion = {
            "idSesion": id_sesion,
            "empresa": {
                "id": empresa_id,
                "nombre": datos_usuario.get("nombreEmpresa", "Empresa Desconocida")
            },
            "usuario": {
                "nombre": datos_usuario.get("nombre", "desconocido"),
                "usuario": usuario_id,
                "rol": datos_usuario.get("rol", "sin rol"),
                "ip": datos_usuario.get("ip", "desconocida"),
                "dispositivo": datos_usuario.get("dispositivo", "desconocido"),
                "sistema": datos_usuario.get("sistema", "desconocido"),
                "navegador": datos_usuario.get("navegador", "desconocido"),
                "idioma": datos_usuario.get("idioma", "desconocido")
            },
            "eventos": [],
            "fechaInicio": ahora
        }
        logs_dia.append(log_sesion)

    # Agregar el nuevo evento
    log_sesion["eventos"].append({
        "fecha": ahora,
        "nivel": nivel,
        "accion": accion,
        "detalle": detalle
    })

    # Si se marca como fin de sesión, calcula duración
    if fin_sesion:
        inicio = datetime.fromisoformat(log_sesion["fechaInicio"].replace("Z", ""))
        fin = datetime.utcnow()
        duracion = fin - inicio
        log_sesion["duracionSesion"] = str(duracion)
        log_sesion["resultadoSesion"] = "cerrada correctamente"
        log_sesion["fechaFin"] = ahora

    # Guardar todo el archivo actualizado
    with open(archivo, "w", encoding="utf-8") as f:
        json.dump(logs_dia, f, indent=2, ensure_ascii=False)

    print(f"✅ Evento guardado en {archivo}")
