from django.db import models
from django.contrib.auth.models import User

class Roles(models.Model):
    rol_nombre = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.rol_nombre

    class Meta: 
        verbose_name= 'Rol'
        verbose_name_plural= 'Roles'
        db_table = 'roles'

class EstadoCivil(models.Model):
    estado_civil = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.estado_civil

    class Meta: 
        verbose_name= 'EstadoCivil'
        verbose_name_plural= 'EstadosCiviles'
        db_table = 'estadoCivil'

class Carreras(models.Model):
    carrera = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.carrera

    class Meta: 
        verbose_name= 'Carrera'
        verbose_name_plural= 'Carreras'
        db_table = 'carreras'


class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.ForeignKey(Roles, on_delete=models.PROTECT, default="1")
    cedula = models.CharField(max_length=10, unique=True)
    fecha_caducidad = models.DateField()
    fecha_nacimiento = models.DateField()
    fecha_ingreso = models.DateField()
    genero = models.CharField(max_length=15, choices=[("M", "Masculino"), ("F", "Femenino")], null=True, blank=True)
    nombramiento = models.CharField(max_length=15, choices=[("Titular", "Titular"), ("Contrato", "A Contrato")])
    lugar_trabajo = models.ForeignKey(Carreras, on_delete=models.CASCADE)
    ciudad = models.CharField(max_length=50)
    direccion = models.TextField()
    telefono = models.CharField(max_length=10)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.CASCADE, default="1")
    estado = models.BooleanField(default=True)
    

    def __str__(self):
        return f"{self.user.username} - {self.cedula}"
    
    class Meta: 
        verbose_name= 'PerfilUsuario'
        verbose_name_plural= 'PerfilesUsuarios'
        db_table = 'perfilUsuario'