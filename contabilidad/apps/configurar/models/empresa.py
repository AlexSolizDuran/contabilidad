from django.db import models
from ...usuario.models.usuario import User

class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    nit = models.PositiveIntegerField(null=True)
    usuario = models.ManyToManyField(User, through='UserEmpresa', related_name='empresas')
    class Meta:
        db_table = "empresa"
        
    def __str__(self):
        return str(self.id) + self.nombre
    
    
class UserEmpresa(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    rol = models.CharField(max_length=50, default='empleado')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    class Meta:
        db_table = "empresa_user"  