from django.db import models

# Create your models here.
class PlantillaRol(models.Model):
    nombre = models.CharField(max_length=20)
    class Meta:
        db_table = "plantilla_rol"