from django.contrib import admin
from .models import Correos, Rol, Usuario, TipoPatron, Patrone, Factura, Compra
from django.utils.html import format_html

#Usuario: admin contraseña: 123456

@admin.register(Rol)
class RolAdmin(admin.ModelAdmin):
    list_display = ('id','NombreRol',)  

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (('cedula', 'nombre', 'apellido', 'correo', 'usuario', 'contrasena', 'NombreRol', 'fotoPerfil', 'verFotoPerfil' ))
    def rol(self, obj):
        return obj.rol.NombreRol

    def verFotoPerfil(sle, obj):
        fotoPerfil = obj.fotoPerfil.url
        return format_html(f"<a href='{fotoPerfil}' target='_blank'><img src='{fotoPerfil} width='30%' />")

@admin.register(TipoPatron)
class TipoPatronAdmin(admin.ModelAdmin):
    list_display = ('id','tipoPatron', 'descripcion',)
    
@admin.register(Patrone)
class PatronAdmin(admin.ModelAdmin):
    list_display = ( 'id','nombreArchivo', 'descripcion', 'precio', 'tipoPatron','archivo','verImagen','creador',)
    def creador(self, obj):
        return obj.usuario.nombre

    def tipoPatron(self, obj):
        return obj.tipopatron.tipoPatron

    def verImagen(self, obj):
        imagen = obj.imagen.url
        return format_html(f"<a href='{imagen}' target='_blank'><img src='{imagen}' width='30%' />")


@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombreArchivo', 'cantidad',  'total', 'fecha', )

    def nombreArchivo(self, obj):
        return obj.patrone.nombreArchivo

@admin.register(Compra)
class CompraAdmin(admin.ModelAdmin):
    list_display = ('id', 'IdFactura', 'usuario', 'descripcion', 'estado', )

    def usuario(self, obj):
       return obj.usuario.cedula

@admin.register(Correos)
class CorreoAdmin(admin.ModelAdmin):
    list_display = ('id','usuario', 'titulo', 'contenido', )

