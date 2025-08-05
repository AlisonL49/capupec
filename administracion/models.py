from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from datetime import datetime
from django.utils import timezone


# Administracion

class Representantes(models.Model):
    presidente = models.CharField(max_length=150)
    administrador = models.CharField(max_length=150)
    secretario = models.CharField(max_length=150)
    tesorero_aso = models.CharField(max_length=150)
    tesorero = models.CharField(max_length=150)
    
    def __str__(self):
        return f"Representantes {self.id}"
    
    class Meta: 
        verbose_name= 'Representante'
        verbose_name_plural= 'Representantes'
        db_table = 'representantes'
 
class Parametros(models.Model):
    parm_abreviatura = models.CharField(max_length=20, unique=True)
    parm_descripcion = models.CharField(max_length=255)
    parm_valor = models.DecimalField(max_digits=10, decimal_places=2)
    parm_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.parm_abreviatura
    
    class Meta: 
        verbose_name= 'Parametro'
        verbose_name_plural= 'Parametros'
        db_table = 'parametros'


class FormasPago(models.Model):
    fpago_codigo = models.CharField(max_length=10, unique=True)
    fpago_descripcion = models.CharField(max_length=255)
    fpago_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.fpago_descripcion
    
    class Meta: 
            verbose_name= 'FormaPago'
            verbose_name_plural= 'FormasPagos'
            db_table = 'formaPagos'

class DestinosCredito(models.Model):
    dest_codigo = models.CharField(max_length=10, unique=True)
    dest_descripcion = models.CharField(max_length=255)
    dest_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.dest_descripcion

    class Meta: 
                verbose_name= 'DestinoCredito'
                verbose_name_plural= 'DestinosCreditos'
                db_table = 'destinosCredito'
      
class PlazoFijo(models.Model):
    pf_descripcion = models.CharField(max_length=255)    
    pf_monto = models.DecimalField(max_digits=10, decimal_places=2)
    pf_plazo = models.IntegerField()
    pf_tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    pf_fecha_vencimiento = models.DateField()
    pf_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.pf_descripcion

    class Meta: 
                verbose_name= 'PLazoFijo'
                verbose_name_plural= 'PlazosFijos'
                db_table = 'plazofijo'
      
class Capitalizaciones (models.Model):
    cap_nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.cap_nombre
    
    class Meta: 
        verbose_name= 'Capitalizacion'
        verbose_name_plural= 'Capitalizaciones'
        db_table = 'capitalizaciones'



class TiposAhorros(models.Model):
    tahorro_abreviatura = models.CharField(max_length=20, unique=True)
    tahorro_tipo = models.CharField(max_length=255)  
    tahorro_dia_aporte = models.IntegerField()
    tahorro_meses_minimo = models.IntegerField()    
    tahorro_porcent_aporte = models.DecimalField(max_digits=5, decimal_places=2)
    tahorro_capitalizacion = models.ForeignKey(Capitalizaciones, on_delete=models.CASCADE)
    tahorro_estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tahorro_tipo

    class Meta: 
                verbose_name= 'TipoAhorro'
                verbose_name_plural= 'TiposAhorros'
                db_table = 'tiposAhorros'

class TiposCredito(models.Model):
    tcredito_abreviatura = models.CharField(max_length=20, unique=True)
    tcredito_tipo= models.CharField(max_length=100)
    tcredito_monto_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    tcredito_tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    tcredito_porcentaje_mora = models.DecimalField(max_digits=5, decimal_places=2)
    tcredito_num_cuotas = models.IntegerField()
    tcredito_aporte_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    tcredito_porcentaje_encaje = models.DecimalField(max_digits=5, decimal_places=2)
    tcredito_gracia = models.IntegerField()
    tcredito_estado = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        self.tcredito_tipo = self.tcredito_tipo.upper().replace(" ", "")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.tcredito_tipo
    
    class Meta: 
                verbose_name= 'TipoCredito'
                verbose_name_plural= 'TiposCreditos'
                db_table = 'tiposCreditos'

class TiposAFuturos(models.Model):
    tafuturo_abreviatura = models.CharField(max_length=15, unique=True)
    tafuturo_tipo = models.CharField(max_length=100)
    tafuturo_v_inicial = models.DecimalField(max_digits=10, decimal_places=2)    
    tafuturo_v_periodico = models.DecimalField(max_digits=10, decimal_places=2)
    tafuturo_penalizacion = models.DecimalField(max_digits=5, decimal_places=2)
    tafuturo_plazo = models.IntegerField()
    #tafuturo_tasa_interes = models.DecimalField(max_digits=5, decimal_places=2)
    tafuturo_estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.tafuturo_tipo

    class Meta: 
                verbose_name= 'TipoAFuturo'
                verbose_name_plural= 'TiposAFuturos'
                db_table = 'tiposAFuturos'

class InteresAhorros(models.Model):
    iahorro_tipo = models.ForeignKey(TiposAhorros, on_delete=models.CASCADE)
    iahorro_rendimiento = models.CharField(max_length=100)
    iahorro_v_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    iahorro_v_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    iahorro_estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.iahorro_tipo

    class Meta: 
                verbose_name= 'InteresAhorro'
                verbose_name_plural= 'InteresAhorros'
                db_table = 'interesAhorros'

class InteresAFuturo(models.Model):
    iafuturo_tipo = models.ForeignKey(TiposAFuturos, on_delete=models.CASCADE)
    iafuturo_rendimiento = models.CharField(max_length=100)
    iafuturo_v_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    iafuturo_v_maximo = models.DecimalField(max_digits=10, decimal_places=2)
    iafuturo_estado = models.BooleanField(default=True)
    
    def __str__(self):
        return self.iafuturo_tipo

    class Meta: 
                verbose_name= 'InteresAFuturo'
                verbose_name_plural= 'InteresAFuturos'
                db_table = 'interesAFuturos'

class PeriodoContable (models.Model):
    periodo_año = models.PositiveIntegerField(default=2000)
    periodo_estado = models.BooleanField(default=True)

    def __str__(self):
        return self.periodo_año
    
    class Meta:
                verbose_name= 'PeriodoContable'
                verbose_name_plural= 'PeriodosContables'
                db_table= 'periodosContables'