from django.db import models


class PlantillaClase(models.Model):
    class Meta:
        db_table ="plantilla_clase"
        
    nombre = models.CharField(max_length=100)
    codigo = models.PositiveIntegerField()
    
    padre = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="hijos"
    )
    
    def save(self, *args, **kwargs):
        codigo_str = str(self.codigo)
        clase_seleccionada = None   

        # Buscamos la clase más específica por prefijo, filtrando por empresa
        for i in range(len(codigo_str), 0, -1):
            prefijo = int(codigo_str[:i])
            try:
                candidata = PlantillaClase.objects.get(codigo=prefijo)
                # Evitar asignarse a sí misma
                if candidata != self:
                    clase_seleccionada = candidata
                    break
            except PlantillaClase.DoesNotExist:
                continue

        self.padre = clase_seleccionada

        super().save(*args, **kwargs)

    
    def __str__(self):
        return self.codigo + " - " + self.nombre