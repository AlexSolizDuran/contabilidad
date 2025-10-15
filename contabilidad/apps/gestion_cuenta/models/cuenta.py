from django.db import models
from django.forms import ValidationError
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
        # 1️⃣ Validar unicidad por código y empresa
        print("si entro al modelo")
        if Cuenta.objects.filter(codigo=self.codigo, empresa=self.empresa).exclude(pk=self.pk).exists():
            raise ValidationError({
                "codigo": "Ya existe una cuenta con este código en la empresa."
            })

        # 2️⃣ Asignar clase_cuenta automáticamente según prefijo (usar strings para no perder ceros)
        codigo_str = str(self.codigo)
        posibles_codigos = [codigo_str[:i+1] for i in range(len(codigo_str))]

        clase = ClaseCuenta.objects.filter(
            codigo__in=posibles_codigos,
            empresa=self.empresa
        ).order_by('-codigo').first()

        self.clase_cuenta = clase  # Puede ser None si no encuentra ninguna

        # 3️⃣ Guardar usando super
        try:
            super().save(*args, **kwargs)
        except ValidationError:
            # Re-lanzar errores de validación de manera que DRF los capture
            raise
        except Exception as e:
            # Captura cualquier otro error inesperado
            raise ValidationError({
                "detail": f"Ocurrió un error al guardar la cuenta: {str(e)}"
            })


    