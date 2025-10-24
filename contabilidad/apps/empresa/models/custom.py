from django.db import models


class Custom(models.Model):
    nombre = models.CharField(max_length=100)
    color_primario = models.CharField(max_length=7)
    color_secundario = models.CharField(max_length=7)
    color_terciario = models.CharField(max_length=7)
    class Meta:
        db_table = "custom"
    
    def __str__(self):
        return self.nombre
