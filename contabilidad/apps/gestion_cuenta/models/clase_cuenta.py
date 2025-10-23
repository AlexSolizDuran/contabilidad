from django.db import models
from ...empresa.models.empresa import Empresa
import uuid

class ClaseCuenta(models.Model):
    class Meta:
        db_table ="clase_cuenta"
        unique_together = ('codigo','empresa')
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
        codigo_str = str(self.codigo)
        clase_seleccionada = None   

        # Buscamos la clase más específica por prefijo, filtrando por empresa
        for i in range(len(codigo_str), 0, -1):
            prefijo = int(codigo_str[:i])
            try:
                candidata = ClaseCuenta.objects.get(codigo=prefijo, empresa=self.empresa)
                # Evitar asignarse a sí misma
                if candidata != self:
                    clase_seleccionada = candidata
                    break
            except ClaseCuenta.DoesNotExist:
                continue

        self.padre = clase_seleccionada

        super().save(*args, **kwargs)


    def get_descendientes_ids(self):
        """
        Devuelve una lista con los IDs de esta clase y todas sus subclases recursivamente
        """
        ids = [self.id]
        for hijo in self.hijos.all():
            ids.extend(hijo.get_descendientes_ids())
        return ids
    def __str__(self):
        return self.codigo + " - " + self.nombre