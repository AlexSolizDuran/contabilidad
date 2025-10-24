from django.db import models
from .empresa import Empresa
from .user_empresa import UserEmpresa
# Create your models here.
class RolEmpresa(models.Model):
    nombre = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,related_name='roles')
    usuarios = models.ManyToManyField(UserEmpresa, related_name='roles')
    class Meta:
        db_table = "rol_empresa"
    
    def __str__(self):
        return f"{self.nombre} - {self.empresa.nombre}"