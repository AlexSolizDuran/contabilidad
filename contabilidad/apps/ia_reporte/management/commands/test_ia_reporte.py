from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from contabilidad.apps.ia_reporte.services import IAReporteService
from contabilidad.apps.empresa.models import Empresa
from contabilidad.apps.empresa.models.user_empresa import UserEmpresa

User = get_user_model()


class Command(BaseCommand):
    help = 'Prueba el sistema de IA para generar reportes'

    def add_arguments(self, parser):
        parser.add_argument(
            '--solicitud',
            type=str,
            help='Solicitud de reporte en lenguaje natural',
            default='Genera un balance general de este año'
        )
        parser.add_argument(
            '--usuario-id',
            type=str,
            help='ID del usuario para la prueba',
            required=True
        )

    def handle(self, *args, **options):
        solicitud = options['solicitud']
        usuario_id = options['usuario_id']
        
        try:
            # Obtener usuario
            usuario = User.objects.get(id=usuario_id)
            self.stdout.write(f"Usuario encontrado: {usuario.email}")
            
            # Obtener empresa del usuario
            try:
                user_empresa = UserEmpresa.objects.get(user=usuario)
                empresa = user_empresa.empresa
                self.stdout.write(f"Empresa: {empresa.nombre}")
            except UserEmpresa.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR('Usuario no está asociado a ninguna empresa')
                )
                return
            
            # Procesar solicitud con IA
            self.stdout.write(f"\nProcesando solicitud: '{solicitud}'")
            self.stdout.write("=" * 50)
            
            servicio_ia = IAReporteService()
            resultado = servicio_ia.procesar_solicitud_reporte(
                texto_solicitud=solicitud,
                usuario=usuario,
                empresa=empresa
            )
            
            if resultado['success']:
                self.stdout.write(
                    self.style.SUCCESS('✅ Reporte generado exitosamente')
                )
                self.stdout.write(f"Tipo de reporte: {resultado['interpretacion']['tipo_reporte']}")
                self.stdout.write(f"Descripción: {resultado['interpretacion']['descripcion_interpretada']}")
                
                if 'fecha_inicio' in resultado['interpretacion'] and resultado['interpretacion']['fecha_inicio']:
                    self.stdout.write(f"Fecha inicio: {resultado['interpretacion']['fecha_inicio']}")
                if 'fecha_fin' in resultado['interpretacion'] and resultado['interpretacion']['fecha_fin']:
                    self.stdout.write(f"Fecha fin: {resultado['interpretacion']['fecha_fin']}")
                
                # Mostrar resumen del reporte
                reporte = resultado['reporte']
                if reporte['tipo'] == 'balance_general':
                    self.stdout.write(f"\n📊 Balance General - Fecha: {reporte['fecha_corte']}")
                    self.stdout.write(f"Activos: {len(reporte['activos'])} clases")
                    self.stdout.write(f"Pasivos: {len(reporte['pasivos'])} clases")
                    self.stdout.write(f"Patrimonio: {len(reporte['patrimonio'])} clases")
                
                elif reporte['tipo'] == 'estado_resultados':
                    self.stdout.write(f"\n📈 Estado de Resultados")
                    self.stdout.write(f"Utilidad Neta: ${reporte['utilidad_neta']:,.2f}")
                
                elif reporte['tipo'] == 'libro_mayor':
                    self.stdout.write(f"\n📚 Libro Mayor")
                    self.stdout.write(f"Cuentas: {len(reporte['cuentas'])}")
                
                elif reporte['tipo'] == 'libro_diario':
                    self.stdout.write(f"\n📖 Libro Diario")
                    self.stdout.write(f"Asientos: {len(reporte['asientos'])}")
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error: {resultado["error"]}')
                )
                
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Usuario con ID {usuario_id} no encontrado')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error inesperado: {str(e)}')
            )
