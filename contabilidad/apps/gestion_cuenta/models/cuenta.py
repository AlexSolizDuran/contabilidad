from django.db import models
from .clase_cuenta import ClaseCuenta
from ...configurar.models.empresa import Empresa

class Cuenta(models.Model):
    ESTADO_CHOICES = [
        ('ACTIVO', 'ACTIVO'),
        ('INACTIVO', 'INACTIVO'),
        ('CERRADO', 'CERRADO'),
    ]
    class Meta:
        db_table = "cuenta"
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
        if not self.clase_cuenta:
            codigo_str = str(self.codigo)
            
            # Buscar la ClaseCuenta cuyo código sea prefijo del código de la cuenta
            clase = ClaseCuenta.objects.filter(
                codigo__in=[int(codigo_str[:i+1]) for i in range(len(codigo_str))]
            ).order_by('-codigo').first()  # Tomar la más específica
            
            self.clase_cuenta = clase  # Puede ser None si no encuentra ninguna

        super().save(*args, **kwargs)

    def __str__(self):
        return self.codigo + " - " + self.nombre
    