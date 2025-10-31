from django.db import models
from .rol import RolEmpresa
class Permiso(models.Model):
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(blank=True, null=True)
    roles = models.ManyToManyField(RolEmpresa, related_name='permisos')
    
    class Meta:
        db_table = "permiso"

    