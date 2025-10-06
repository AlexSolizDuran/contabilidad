from django.db import models
from ...usuario.models.usuario import User
from .empresa import Empresa
from .custom import Custom

        
class UserEmpresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    custom = models.ForeignKey(Custom, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  
    class Meta:
        db_table = "user_empresa"  
        unique_together = ('usuario', 'empresa')
        