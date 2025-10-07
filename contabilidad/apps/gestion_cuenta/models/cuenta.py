from django.db import models
from .clase_cuenta import ClaseCuenta
from ...empresa.models.empresa import Empresa
import uuid

class Cuenta(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
        ('CERRADO', 'CERRADO'),
    ]
    class Meta:
        db_table = "cuenta"
        unique_together = ('codigo','empresa')
        
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.PositiveBigIntegerField()
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=10 , choices=ESTADO_CHOICES, default='ACTIVO')
    clase_cuenta = models.ForeignKey(
        ClaseCuenta,
        on_delete=models.SET_NULL,
        blank=True,null=True,
        related_name="cuentas"
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="cuentas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        codigo_str = str(self.codigo)

        # Generar lista de posibles prefijos
        posibles_codigos = [int(codigo_str[:i+1]) for i in range(len(codigo_str))]

        # Buscar la ClaseCuenta más específica según prefijo y empresa
        clase = ClaseCuenta.objects.filter(
            codigo__in=posibles_codigos,
            empresa=self.empresa
        ).order_by('-codigo').first()

        self.clase_cuenta = clase  # Puede ser None si no encuentra ninguna

        super().save(*args, **kwargs)


    