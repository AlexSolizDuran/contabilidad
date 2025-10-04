from django.db import models
class AsientoContable(models.Model):
    ESTADO_CHOICES = [
        ('BORRADOR','BORRADOR'),
        ('APROBADO','APROBADO'),
        ('CANCELADO','CANCELADO'),        
    ]
    class Meta:
        db_table = "asiento_contable"
    
    numero = models.PositiveIntegerField()
    descripcion = models.CharField(max_length=100)
    estado = models.CharField(max_length=10,choices=ESTADO_CHOICES,default='BORRADOR')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)