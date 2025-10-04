from django.db import models
from ...gestion_cuenta.models.cuenta import Cuenta
from .asiento_contable import AsientoContable
class Movimiento(models.Model):
    class Meta:
        db_table = "movimiento"
    
    referencia = models.CharField(max_length=100)
    debe = models.DecimalField(max_digits=10,decimal_places=3)
    haber = models.DecimalField(max_digits=10,decimal_places=3)
    cuenta = models.ForeignKey(
        Cuenta,
        on_delete=models.CASCADE,
        related_name="movimientos"
    )
    asiento_contable = models.ForeignKey(
        AsientoContable,
        on_delete=models.CASCADE,
        related_name="movimientos"
    )