from distutils.command.upload import upload
from email.policy import default
from django.db import models

class Rol(models.Model):
    NombreRol = models.CharField( max_length=20, default="Cliente")
    def __str__(self):
        return self.NombreRol

class Usuario(models.Model):
    cedula = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=254)
    apellido = models.CharField(max_length=254)
    correo = models.EmailField(max_length=254, unique=True)
    usuario = models.CharField(max_length=20, unique=True)
    contrasena = models.CharField(max_length=10)
    NombreRol = models.ForeignKey(Rol, on_delete= models.DO_NOTHING)
    fotoPerfil = models.ImageField(upload_to = 'DesignCal/fotosPerfil', default= 'DesignCal/fotosPerfil/default.jpg')
    def __str__(self): 
       return self.nombre

class TipoPatron(models.Model):
    tipoPatron = models.CharField(max_length=254)
    descripcion = models.TextField(default='Pendiente')
    def __str__(self):
        return self.tipoPatron

class Patrone(models.Model):
    nombreArchivo = models.CharField(max_length=200)
    descripcion = models.TextField(default='Pendiente')
    precio = models.BigIntegerField(default=0)
    usuario = models.ForeignKey(Usuario, on_delete= models.DO_NOTHING)
    tipoPatron = models.ForeignKey(TipoPatron, on_delete= models.DO_NOTHING)
    archivo = models.FileField(upload_to = 'DesignCal/files', default= None)
    imagen = models.ImageField(upload_to = 'DesignCal/fotos', default = 'DesignCal/fotos/default.jpg')
    
    def __str__(self):
        return self.nombreArchivo

class Factura(models.Model):
    nombreArchivo = models.ForeignKey(Patrone, on_delete= models.DO_NOTHING)
    cantidad = models.SmallIntegerField(default=0)
    total = models.BigIntegerField(default=0)
    fecha = models.DateTimeField()
    def __str__(self):
        return str(self.pk)

class Compra(models.Model):
    IdFactura = models.ForeignKey(Factura, on_delete= models.DO_NOTHING, default= 0)
    usuario = models.ForeignKey(Usuario, on_delete= models.DO_NOTHING)
    descripcion = models.CharField(max_length=250, default='Pendiente')
    estados = (
        ("P", "Pendiente"),
        ("CP", "Completo"),
        ("C", "Cancelado"),
    )
    estado = models.CharField(choices=estados, max_length=2, default="P")
    def __str__(self):
        return str(self.pk)

class Correos(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete= models.DO_NOTHING)
    titulo = models.CharField(max_length=250, unique=True)
    contenido = models.CharField(max_length=254)
    def __str__(self):
        return str(self.titulo)

