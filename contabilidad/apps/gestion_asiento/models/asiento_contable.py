from django.db import models
from ...empresa.models import Empresa
import uuid

class AsientoContable(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR','BORRADOR'),
        ('APROBADO','APROBADO'),
        ('CANCELADO','CANCELADO'),        
    ]
    class Meta:
        db_table = "asiento_contable"
        
    id = models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    numero = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=100)
    empresa = models.ForeignKey(Empresa,on_delete=models.CASCADE,related_name='asientos')
    estado = models.CharField(max_length=10,choices=ESTADO_CHOICES,default='BORRADOR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)