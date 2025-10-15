from django.db import models
from ..models.user_empresa import UserEmpresa

class Favorito(models.Model):
    class Meta:
        db_table = 'favorito'
    user_empresa = models.ForeignKey(UserEmpresa, on_delete=models.CASCADE,related_name='favoritos')
    ruta = models.CharField(max_length=255)
    nombre = models.CharField(max_length=255)
    
    
