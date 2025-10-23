from django.db import models
from django.forms import ValidationError
from .plantilla_clase import PlantillaClase

class PlantillaCuenta(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
        ('CERRADO', 'CERRADO'),
    ]
    
    class Meta:
        db_table = "plantilla_cuenta"
        
    codigo = models.PositiveBigIntegerField()
    nombre = models.CharField(max_length=100)
    estado = models.CharField(max_length=10 , choices=ESTADO_CHOICES, default='ACTIVO')
    clase_cuenta = models.ForeignKey(
        PlantillaClase,
        on_delete=models.SET_NULL,
        blank=True,null=True,
        related_name="cuentas"
    )
    
    def save(self, *args, **kwargs):
        # 1️⃣ Validar unicidad por código y empresa
        if PlantillaCuenta.objects.filter(codigo=self.codigo).exclude(pk=self.pk).exists():
            raise ValidationError({
                "codigo": "Ya existe una cuenta con este código en la empresa."
            })

        # 2️⃣ Asignar clase_cuenta automáticamente según prefijo (usar strings para no perder ceros)
        codigo_str = str(self.codigo)
        posibles_codigos = [codigo_str[:i+1] for i in range(len(codigo_str))]

        clase = PlantillaClase.objects.filter(
            codigo__in=posibles_codigos,
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


    