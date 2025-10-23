from django.db import models
from ...usuario.models.usuario import User
import uuid


class Empresa(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(max_length=100)
    nit = models.PositiveIntegerField(null=True)
    usuarios = models.ManyToManyField(User, through='UserEmpresa', related_name='empresas')
    class Meta:
        db_table = "empresa"
        
    def __str__(self):
        return f"{self.nombre} ({self.nit})"
    
    
