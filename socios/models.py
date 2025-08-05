from django.db import models

 
class SimulacionCredito(models.Model):
    TIPOS_CREDITO = [
        ('educacion', 'Educación'),
        ('vacaciones', 'Vacaciones'),
        ('construccion', 'Construcción'),
        ('emergencia', 'Emergencia'),
    ]
    
    simu_nombre = models.CharField(max_length=100)
    simu_tipo_credito = models.CharField(max_length=20, choices=TIPOS_CREDITO)
    simu_monto = models.DecimalField(max_digits=10, decimal_places=2)
    simu_meses = models.IntegerField()
    simu_interes_anual = models.DecimalField(max_digits=5, decimal_places=2, default=12.0)  # 12% por defecto
    
    def calcular_amortizacion_francesa(self):
        """Calcula la cuota mensual con amortización francesa"""
        tasa_mensual = (self.interes_anual / 100) / 12
        cuota = self.simu_monto * (tasa_mensual * (1 + tasa_mensual) ** self.simu_meses) / ((1 + tasa_mensual) ** self.simu_meses - 1)
        monto_total = cuota * self.simu_meses
        return round(cuota, 2), round(monto_total, 2)
    
    def __str__(self):
        return f"{self.simu_nombre} - {self.simu_tipo_credito}"
    
    
    class Meta: 
                verbose_name= 'Simulacion'
                verbose_name_plural= 'Simulaciones'
                db_table = 'simulaciones'
