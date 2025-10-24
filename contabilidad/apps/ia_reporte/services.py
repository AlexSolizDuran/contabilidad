import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from django.db.models import Q, Sum, F
from django.conf import settings
from openai import OpenAI
from django.db.models import Sum
from datetime import datetime

from .config import IAConfig
from contabilidad.apps.gestion_cuenta.models import Cuenta, ClaseCuenta
from contabilidad.apps.gestion_asiento.models import AsientoContable, Movimiento
from contabilidad.apps.empresa.models import Empresa
from contabilidad.apps.usuario.models import User


class IAReporteService:
    """
    Servicio de IA para interpretar solicitudes de reportes en lenguaje natural
    y generar reportes basados en los datos del usuario y empresa.
    """
    
    def __init__(self):
        if IAConfig.is_openai_configured():
            self.client = OpenAI(api_key=IAConfig.OPENAI_API_KEY)
        else:
            self.client = None
        
    def procesar_solicitud_reporte(self, texto_solicitud: str, usuario: User, empresa: Empresa) -> Dict[str, Any]:
        """
        Procesa una solicitud de reporte en lenguaje natural y genera el reporte correspondiente.
        
        Args:
            texto_solicitud: Texto en lenguaje natural con la solicitud del reporte
            usuario: Usuario autenticado
            empresa: Empresa del usuario
            
        Returns:
            Dict con el reporte generado y metadatos
        """
        try:
            # 1. Interpretar la solicitud con IA
            interpretacion = self._interpretar_solicitud(texto_solicitud, empresa)
            
            # 2. Generar el reporte basado en la interpretación
            reporte = self._generar_reporte(interpretacion, empresa)
            
            # 3. Formatear la respuesta
            return {
                'success': True,
                'solicitud_original': texto_solicitud,
                'interpretacion': interpretacion,
                'reporte': reporte,
                'fecha_generacion': datetime.now().isoformat(),
                'empresa': empresa.nombre
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'solicitud_original': texto_solicitud
            }
    
    def _interpretar_solicitud(self, texto: str, empresa: Empresa) -> Dict[str, Any]:
        """
        Usa IA para interpretar la solicitud de reporte y extraer parámetros.
        """
        # Obtener contexto de la empresa
        contexto_empresa = self._obtener_contexto_empresa(empresa)
        
        prompt = f"""
        Eres un asistente contable especializado en interpretar solicitudes de reportes.
        
        CONTEXTO DE LA EMPRESA:
        {contexto_empresa}
        
        SOLICITUD DEL USUARIO: "{texto}"
        
        Analiza la solicitud y extrae la siguiente información en formato JSON:
        {{
            "tipo_reporte": "balance_general|estado_resultados|libro_mayor|libro_diario|analisis_cuentas|otro",
            "fecha_inicio": "YYYY-MM-DD o null si no se especifica",
            "fecha_fin": "YYYY-MM-DD o null si no se especifica", 
            "cuentas_especificas": ["lista de códigos de cuentas si se mencionan"],
            "clases_cuentas": ["lista de códigos de clases si se mencionan"],
            "filtros_adicionales": {{
                "estado_asientos": "BORRADOR|APROBADO|CANCELADO o null",
                "monto_minimo": "número o null",
                "monto_maximo": "número o null"
            }},
            "agrupacion": "por_cuenta|por_clase|por_fecha|por_asiento",
            "ordenamiento": "ascendente|descendente",
            "descripcion_interpretada": "descripción clara de lo que se solicita"
        }}
        
        IMPORTANTE:
        - Si no se especifica fecha, usar el año actual completo
        - Si se menciona "último mes", calcular desde hace 30 días
        - Si se menciona "este año", usar desde enero 1 hasta hoy
        - Si se menciona "trimestre", calcular el trimestre actual
        """
        
        try:
            if not self.client:
                raise ValueError("OpenAI no está configurado")
                
            response = self.client.chat.completions.create(
                model=IAConfig.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un experto contable que interpreta solicitudes de reportes."},
                    {"role": "user", "content": prompt}
                ],
                temperature=IAConfig.OPENAI_TEMPERATURE,
                max_tokens=IAConfig.OPENAI_MAX_TOKENS
            )
            
            interpretacion_texto = response.choices[0].message.content
            # Extraer JSON de la respuesta
            json_match = re.search(r'\{.*\}', interpretacion_texto, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                raise ValueError("No se pudo extraer JSON de la respuesta de IA")
                
        except Exception as e:
            # Fallback: interpretación básica sin IA
            return self._interpretacion_basica(texto)
    
    def _obtener_contexto_empresa(self, empresa: Empresa) -> str:
        """
        Obtiene información contextual de la empresa para la IA.
        """
        cuentas = Cuenta.objects.filter(empresa=empresa, estado='ACTIVO')
        clases = ClaseCuenta.objects.filter(empresa=empresa)
        
        contexto = f"""
        EMPRESA: {empresa.nombre}
        NIT: {empresa.nit}
        
        CLASES DE CUENTAS DISPONIBLES:
        """
        
        for clase in clases[:10]:  # Limitar a 10 para no sobrecargar
            contexto += f"- {clase.codigo}: {clase.nombre}\n"
        
        contexto += "\nCUENTAS PRINCIPALES:\n"
        limite = IAConfig.get_contexto_empresa_limitado()
        for cuenta in cuentas[:limite]:
            contexto += f"- {cuenta.codigo}: {cuenta.nombre}\n"
        
        return contexto
    
    def _interpretacion_basica(self, texto: str) -> Dict[str, Any]:
        """
        Interpretación básica sin IA como fallback.
        """
        texto_lower = texto.lower()
        
        # Detectar tipo de reporte
        if any(palabra in texto_lower for palabra in ['balance', 'general', 'situación financiera']):
            tipo = 'balance_general'
        elif any(palabra in texto_lower for palabra in ['resultados', 'pérdidas', 'ganancias', 'utilidad']):
            tipo = 'estado_resultados'
        elif any(palabra in texto_lower for palabra in ['mayor', 'libro mayor']):
            tipo = 'libro_mayor'
        elif any(palabra in texto_lower for palabra in ['diario', 'libro diario']):
            tipo = 'libro_diario'
        else:
            tipo = 'otro'
        
        # Detectar fechas
        fecha_inicio = None
        fecha_fin = None
        
        if 'último mes' in texto_lower:
            fecha_fin = datetime.now()
            fecha_inicio = fecha_fin - timedelta(days=30)
        elif 'este año' in texto_lower:
            fecha_inicio = datetime(datetime.now().year, 1, 1)
            fecha_fin = datetime.now()
        elif 'trimestre' in texto_lower:
            mes_actual = datetime.now().month
            trimestre = (mes_actual - 1) // 3 + 1
            fecha_inicio = datetime(datetime.now().year, (trimestre - 1) * 3 + 1, 1)
            fecha_fin = datetime.now()
        
        return {
            'tipo_reporte': tipo,
            'fecha_inicio': fecha_inicio.strftime('%Y-%m-%d') if fecha_inicio else None,
            'fecha_fin': fecha_fin.strftime('%Y-%m-%d') if fecha_fin else None,
            'cuentas_especificas': [],
            'clases_cuentas': [],
            'filtros_adicionales': {
                'estado_asientos': 'APROBADO',
                'monto_minimo': None,
                'monto_maximo': None
            },
            'agrupacion': 'por_cuenta',
            'ordenamiento': 'ascendente',
            'descripcion_interpretada': f'Reporte de {tipo} solicitado'
        }
    
    def _generar_reporte(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera el reporte basado en la interpretación de la IA.
        """
        tipo_reporte = interpretacion.get('tipo_reporte', 'otro')
        
        if tipo_reporte == 'balance_general':
            return self._generar_balance_general(interpretacion, empresa)
        elif tipo_reporte == 'estado_resultados':
            return self._generar_estado_resultados(interpretacion, empresa)
        elif tipo_reporte == 'libro_mayor':
            return self._generar_libro_mayor(interpretacion, empresa)
        elif tipo_reporte == 'libro_diario':
            return self._generar_libro_diario(interpretacion, empresa)
        else:
            return self._generar_reporte_personalizado(interpretacion, empresa)
    
    def _generar_balance_general(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera un balance general.
        """
        fecha_fin = interpretacion.get('fecha_fin')
        if not fecha_fin:
            fecha_fin = datetime.now().replace(hour=23, minute=59, second=59, microsecond=999999)
        else:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
            fecha_fin = fecha_fin.replace(hour=23, minute=59, second=59, microsecond=999999)
        
        # Obtener saldos de cuentas
        movimientos = Movimiento.objects.filter(
            asiento_contable__empresa=empresa,
            asiento_contable__estado__iexact='APROBADO',
            asiento_contable__created_at__lte=fecha_fin
        ).values('cuenta').annotate(
            total_debe=Sum('debe'),
            total_haber=Sum('haber')
        )
      
        cuentas_saldos = {}
        for mov in movimientos:
            cuenta_id = mov['cuenta']
            saldo = (mov['total_debe'] or 0) - (mov['total_haber'] or 0)
            cuentas_saldos[cuenta_id] = saldo
        
        print(cuentas_saldos)
        # Agrupar por clases - CORRECCIÓN AQUÍ
    
        # Se obtienen todas las clases de cuenta que empiecen por '1' (Activo)
        clases_activo = ClaseCuenta.objects.filter(
            empresa=empresa,
            codigo='1' 
        )
        
        # Se obtienen todas las clases de cuenta que empiecen por '2' (Pasivo)
        clases_pasivo = ClaseCuenta.objects.filter(
            empresa=empresa,
            codigo='2'
        )
        
        # Se obtienen todas las clases de cuenta que empiecen por '3' (Patrimonio)
        clases_patrimonio = ClaseCuenta.objects.filter(
            empresa=empresa,
            codigo='3'
        )
    
        return {
            'tipo': 'balance_general',
            'fecha_corte': fecha_fin.strftime('%Y-%m-%d'),
            'activos': self._calcular_totales_por_clases(clases_activo, cuentas_saldos),
            'pasivos': self._calcular_totales_por_clases(clases_pasivo, cuentas_saldos),
            'patrimonio': self._calcular_totales_por_clases(clases_patrimonio, cuentas_saldos)
        }
    
    def _generar_estado_resultados(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera un estado de resultados.
        """
        # === INICIO CORRECCIÓN DE FECHA INICIO ===
        fecha_inicio_str = interpretacion.get('fecha_inicio')
        if not fecha_inicio_str:
            fecha_inicio = datetime(datetime.now().year, 1, 1).replace(hour=0, minute=0, second=0)
        else:
            fecha_inicio = datetime.strptime(fecha_inicio_str, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
        # === FIN CORRECCIÓN ===

        # === INICIO CORRECCIÓN DE FECHA FIN ===
        fecha_fin_str = interpretacion.get('fecha_fin')
        if not fecha_fin_str:
            fecha_fin = datetime.now().replace(hour=23, minute=59, second=59)
        else:
            fecha_fin = datetime.strptime(fecha_fin_str, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        # === FIN CORRECCIÓN ===

        # === INICIO CORRECCIÓN DE CLASES ===
        # Solo necesitamos pasar la clase raíz. La otra función buscará la jerarquía.

        # Ingresos (clase 4)
        ingresos = self._calcular_movimientos_por_clase(empresa, ['4'], fecha_inicio, fecha_fin)

        # Costos y gastos (clase 5)
        costos_gastos = self._calcular_movimientos_por_clase(empresa, ['5'], fecha_inicio, fecha_fin)
        # === FIN CORRECCIÓN DE CLASES ===

        # Ajusta esto según tu lógica contable
        # Asumimos que los ingresos (4) son Haber (positivos) y Costos (5) son Debe (positivos)
        # La consulta (debe - haber) dará negativo para Ingresos y positivo para Costos.
        # Por eso multiplicamos por -1.
        total_ingresos = ingresos['total'] * -1 
        total_costos_gastos = costos_gastos['total']

        # A_generar_estado_resultadosjusta tus cálculos de utilidad según necesites.
        # Esto es solo un ejemplo.
        utilidad_bruta = total_ingresos - total_costos_gastos 
        utilidad_operacional = utilidad_bruta # Añadir gastos operacionales si los separas
        utilidad_neta = utilidad_operacional # Añadir impuestos, etc.

        return {
            'tipo': 'estado_resultados',
            'periodo': {
            'inicio': fecha_inicio.strftime('%Y-%m-%d'),
                'fin': fecha_fin.strftime('%Y-%m-%d')
            },
            'ingresos': ingresos,
            'costos_gastos': costos_gastos,
            'utilidad_bruta': utilidad_bruta,
            'utilidad_operacional': utilidad_operacional,
            'utilidad_neta': utilidad_neta
        }
    
    def _generar_libro_mayor(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera un libro mayor.
        """
        fecha_inicio = interpretacion.get('fecha_inicio')
        fecha_fin = interpretacion.get('fecha_fin')
        cuentas_especificas = interpretacion.get('cuentas_especificas', [])
        
        if not fecha_inicio:
            fecha_inicio = datetime(datetime.now().year, 1, 1).replace(hour=0, minute=0, second=0)
        else:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').replace(hour=0, minute=0, second=0)
            
        if not fecha_fin:
            fecha_fin = datetime.now().replace(hour=23, minute=59, second=59)
        else:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').replace(hour=23, minute=59, second=59)
        
        # Filtrar cuentas
        cuentas_query = Cuenta.objects.filter(empresa=empresa, estado='ACTIVO')
        
        if cuentas_especificas:
            cuentas_query = cuentas_query.filter(codigo__in=cuentas_especificas)
        
        cuentas_detalle = []
        
        for cuenta in cuentas_query:
            movimientos = Movimiento.objects.filter(
                cuenta=cuenta,
                asiento_contable__empresa=empresa,
                asiento_contable__estado='APROBADO',
                asiento_contable__created_at__range=[fecha_inicio, fecha_fin]
            ).order_by('asiento_contable__created_at')
            
            if movimientos.exists():
                total_debe = sum(m.debe for m in movimientos)
                total_haber = sum(m.haber for m in movimientos)
                saldo = total_debe - total_haber
                
                cuentas_detalle.append({
                    'cuenta': {
                        'codigo': cuenta.codigo,
                        'nombre': cuenta.nombre
                    },
                    'saldo_inicial': 0,  # Se podría calcular si se necesita
                    'total_debe': float(total_debe),
                    'total_haber': float(total_haber),
                    'saldo_final': float(saldo),
                    'movimientos': [
                        {
                            'fecha': m.asiento_contable.created_at.strftime('%Y-%m-%d'),
                            'asiento': m.asiento_contable.numero,
                            'descripcion': m.asiento_contable.descripcion,
                            'referencia': m.referencia,
                            'debe': float(m.debe),
                            'haber': float(m.haber)
                        }
                        for m in movimientos
                    ]
                })
        
        return {
            'tipo': 'libro_mayor',
            'periodo': {
                'inicio': fecha_inicio.strftime('%Y-%m-%d'),
                'fin': fecha_fin.strftime('%Y-%m-%d')
            },
            'cuentas': cuentas_detalle
        }
    
    def _generar_libro_diario(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera un libro diario.
        """
        fecha_inicio = interpretacion.get('fecha_inicio')
        fecha_fin = interpretacion.get('fecha_fin')
        
        if not fecha_inicio:
            fecha_inicio = datetime(datetime.now().year, 1, 1)
        else:
            fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
            
        if not fecha_fin:
            fecha_fin = datetime.now()
        else:
            fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
        
        asientos = AsientoContable.objects.filter(
            empresa=empresa,
            estado='APROBADO',
            created_at__range=[fecha_inicio, fecha_fin]
        ).order_by('created_at')
        
        asientos_detalle = []
        
        for asiento in asientos:
            movimientos = Movimiento.objects.filter(asiento_contable=asiento)
            
            asientos_detalle.append({
                'numero': asiento.numero,
                'fecha': asiento.created_at.strftime('%Y-%m-%d'),
                'descripcion': asiento.descripcion,
                'movimientos': [
                    {
                        'cuenta_codigo': m.cuenta.codigo,
                        'cuenta_nombre': m.cuenta.nombre,
                        'referencia': m.referencia,
                        'debe': float(m.debe),
                        'haber': float(m.haber)
                    }
                    for m in movimientos
                ]
            })
        
        return {
            'tipo': 'libro_diario',
            'periodo': {
                'inicio': fecha_inicio.strftime('%Y-%m-%d'),
                'fin': fecha_fin.strftime('%Y-%m-%d')
            },
            'asientos': asientos_detalle
        }
    
    def _generar_reporte_personalizado(self, interpretacion: Dict[str, Any], empresa: Empresa) -> Dict[str, Any]:
        """
        Genera un reporte personalizado basado en la interpretación.
        """
        # Implementar lógica para reportes personalizados
        return {
            'tipo': 'personalizado',
            'mensaje': 'Reporte personalizado en desarrollo',
            'interpretacion': interpretacion
        }
    
    def _calcular_totales_por_clases(self, clases, cuentas_saldos):
        """
        Calcula totales por clases de cuentas, manejando jerarquía.
        """
        resultado = []
        for clase in clases:
            cuentas_clase = Cuenta.objects.filter(
                clase_cuenta__codigo__startswith=clase.codigo, 
                clase_cuenta__empresa=clase.empresa, # Asegura que sea de la misma empresa
                estado='ACTIVO'
            )

            total_clase = 0
            cuentas_detalle = []

            for cuenta in cuentas_clase:
                saldo = cuentas_saldos.get(cuenta.id, 0)
                if saldo != 0:
                    cuentas_detalle.append({
                        'codigo': cuenta.codigo,
                        'nombre': cuenta.nombre,
                        'saldo': float(saldo)
                        })
                    total_clase += saldo
            if cuentas_detalle:
                resultado.append({
                'clase': {
                        'codigo': clase.codigo,
                        'nombre': clase.nombre
                },
                    'total': float(total_clase),
                    'cuentas': cuentas_detalle
                })

        return resultado
    
    def _calcular_movimientos_por_clase(self, empresa, codigos_clases, fecha_inicio, fecha_fin):
        """
        Calcula movimientos por clase de cuenta en un período.
        """
        clases = ClaseCuenta.objects.filter(
            empresa=empresa,
            codigo__in=codigos_clases # Esto ahora solo recibirá ['4'] o ['5']
        )

        total = 0
        detalle = []

        for clase in clases:
            # === INICIO DE LA CORRECCIÓN ===
            # Buscar todas las cuentas cuya clase_cuenta COMIENCE CON el código de la clase raíz
            cuentas = Cuenta.objects.filter(
                clase_cuenta__codigo__startswith=clase.codigo,
                clase_cuenta__empresa=empresa, # Asegurar la empresa
                estado='ACTIVO'
            )
            # === FIN DE LA CORRECCIÓN ===

            movimientos = Movimiento.objects.filter(
                cuenta__in=cuentas,
                asiento_contable__empresa=empresa,
                asiento_contable__estado='APROBADO',
                # El rango de fechas ahora incluye el día completo
                asiento_contable__created_at__range=[fecha_inicio, fecha_fin] 
            )

            # (Debe - Haber)
            total_clase = sum(m.debe - m.haber for m in movimientos)
            total += total_clase

            if total_clase != 0:
                detalle.append({
                        'clase': {
                        'codigo': clase.codigo,
                        'nombre': clase.nombre
                    },
                    'total': float(total_clase)
                    })

            return {
                'total': float(total),
                'detalle': detalle
            }
