import os
import json
import uuid
from datetime import datetime
import tempfile
import shutil

LOG_DIR = "logs"

class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, uuid.UUID):
            return str(obj)
        return super().default(obj)

def registrar_evento(id_sesion, empresa_id=None, usuario_id=None, datos_usuario=None,
                     nivel="INFO", accion="", detalle="", fin_sesion=False):
    """
    Registrar un evento en el log del usuario.
    Si datos_usuario se pasa y no existe la sesión, crea la sesión.
    Si solo se pasa id_sesion (y opcional empresa_id/usuario_id), agrega el evento a la sesión existente.
    """
    ahora = datetime.utcnow().isoformat() + "Z"

    # Construir ruta del archivo si tenemos empresa y usuario
    if empresa_id and usuario_id:
        carpeta_usuario = os.path.join(LOG_DIR, empresa_id)
        os.makedirs(carpeta_usuario, exist_ok=True)
        archivo = os.path.join(carpeta_usuario, f"{usuario_id}.json")
    else:
        # Si no se envía empresa_id/usuario_id, buscar la sesión por id_sesion
        archivo = None
        for root, dirs, files in os.walk(LOG_DIR):
            for file in files:
                if file.endswith(".json"):
                    posible_archivo = os.path.join(root, file)
                    try:
                        with open(posible_archivo, "r", encoding="utf-8") as f:
                            logs = json.load(f)
                        if any(log["idSesion"] == str(id_sesion) for log in logs):
                            archivo = posible_archivo
                            break
                    except json.JSONDecodeError:
                        continue
            if archivo:
                break
        if not archivo:
            print("⚠️ No se encontró sesión y no se pasaron datos de usuario. Evento ignorado.")
            return

    # Cargar logs existentes
    try:
        with open(archivo, "r", encoding="utf-8") as f:
            logs_usuario = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        logs_usuario = []

    # Buscar sesión existente
    log_sesion = next((log for log in logs_usuario if log["idSesion"] == str(id_sesion)), None)

    # Crear sesión si no existe y se pasan datos_usuario
    if not log_sesion and datos_usuario:
        log_sesion = {
            "idSesion": str(id_sesion),
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
                "idioma": datos_usuario.get("idioma", "desconocido"),
            },
            "eventos": [],
            "fechaInicio": ahora
        }
        logs_usuario.append(log_sesion)

    # Registrar evento
    log_sesion["eventos"].append({
        "fecha": ahora,
        "nivel": nivel,
        "accion": accion,
        "detalle": detalle
    })

    # Cerrar sesión
    if fin_sesion:
        inicio = datetime.fromisoformat(log_sesion["fechaInicio"].replace("Z", ""))
        duracion = datetime.utcnow() - inicio
        log_sesion["fechaFin"] = ahora
        log_sesion["duracionSesion"] = str(duracion)
        log_sesion["resultadoSesion"] = "cerrada correctamente"

    # Guardar cambios
    with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as tmp:
        json.dump(logs_usuario, tmp, indent=2, ensure_ascii=False, cls=UUIDEncoder)
        temp_name = tmp.name
    shutil.move(temp_name, archivo)

    print(f"✅ Evento guardado en {archivo}")
