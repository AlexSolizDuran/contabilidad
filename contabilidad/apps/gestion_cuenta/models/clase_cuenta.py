from django.db import models
from ...configurar.models.empresa import Empresa
class ClaseCuenta(models.Model):
    class Meta:
        
        db_table ="clase_cuenta"
    nombre = models.CharField(max_length=100)
    codigo = models.PositiveIntegerField()
    padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="hijos"
    )
    empresa = models.ForeignKey(
        Empresa,
        on_delete=models.CASCADE,
        related_name="clase_cuentas"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.id:
            codigo_str = str(self.codigo)
            clase_seleccionada = None
            for i in range(len(codigo_str), 0, -1):
                prefijo = int(codigo_str[:i])
                try:
                    clase_seleccionada = ClaseCuenta.objects.get(codigo=prefijo)
                    break  # se encontró la clase más específica existente
                except ClaseCuenta.DoesNotExist:
                    continue
            
            self.padre= clase_seleccionada

        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.codigo + " - " + self.nombre