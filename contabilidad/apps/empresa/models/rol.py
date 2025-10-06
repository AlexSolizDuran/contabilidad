from django.db import models
from .empresa import Empresa
from .user_empresa import UserEmpresa
# Create your models here.
class RolEmpresa(models.Model):
    nombre = models.CharField(max_length=20)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE,related_name='roles')
    usuarios = models.ManyToManyField(UserEmpresa, related_name='roles')
    