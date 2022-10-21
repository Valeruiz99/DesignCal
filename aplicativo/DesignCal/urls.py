from django.urls import path
from . import views

app_name = "DesignCal"

urlpatterns = [
    #_____________________________________________________
    #Index
    path('', views.index, name='index'),
    #_____________________________________________________
    #Login
    path('loginFormulario/', views.loginFormulario, name='login-formulario'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    #_____________________________________________________
    #Patrones
    path('Patrones/', views.listarPatron, name='patron'),
    path('Patron-add/', views.insertarPatron, name='patron-add'),
    path('Patron-guardar/', views.guardarPatron, name='patron-guardar'),
    path('Patron-eliminar/<int:id>', views.eliminarPatron, name='patron-eliminar'),
    path('Patron-editar/<int:id>', views.editarPatron, name="patron-editar"),
    path('Patron-actualizar/', views.actualizarPatron, name="patron-actualizar"),
    path('Patron-buscar/', views.buscarPatron, name="patron-buscar"),
    path('Patrones-tarjetas/', views.tarjetasPatrones, name='patrones'),
    #_____________________________________________________
    #Usuarios
    path('usuario/', views.listarUsuarios, name='usuario'),
    path('usuario-add/', views.agregarUsuarios, name='usuario-add'),
    path('usuario-guardar/', views.guardarUsuario, name='usuario-guardar'),
    path('usuario-eliminar/<int:cedula>', views.eliminarUsuario, name='usuario-eliminar'),
    path('usuario-editar/<int:cedula>', views.editarUsuario, name='usuario-editar'),
    path('usuario-actualizar/', views.actualizarUsuario, name='usuario-actualizar'),
    path('usuario-buscar/', views.buscarUsuario, name='usuario-buscar'),
    path('perfil/', views.perfil, name='usuario-perfil'),
    path('actualizarPerfil/', views.actualizarPerfil, name='usuario-actualizarPerfil'),
    #______________________________________________________________________________________
    #Roles
    path('roles/', views.listarRoles, name='roles'),
    path('rol-add/', views.crearRol, name='rol-add'),
    path('rol-guardar/', views.guardarRol, name='rol-guardar'),
    path('rol-eliminar/<int:id>', views.eliminarRol, name='rol-eliminar'),
    path('rol-editar/<int:id>', views.editarRol, name='rol-editar'),
    path('rol-actualizar/', views.actualizarRol, name='rol-actualizar'),
    path('rol-buscar/', views.buscarRol, name='rol-buscar'),
    #______________________________________________________________________________________
    #Facturas
    path('facturas/', views.listarFacturas, name='facturas'),
    path('facturas-add/', views.agregarFactura, name='facturas-add'),
    path('facturas-guardar/', views.guardarFactura, name='facturas-guardar'),
    path('facturas-buscar/', views.buscarFactura, name='facturas-buscar'),
    #______________________________________________________________________________________
    #Tipo_Patrón
    path('tipoPatron/', views.listartipoPatron, name='tipoPatron'),
    path('tipoPatron-add/', views.creartipoPatron, name='tipoPatron-add'),
    path('tipoPatron-guardar/', views.guardartipoPatron, name='tipoPatron-guardar'),
    path('tipoPatron-eliminar/<int:id>', views.eliminartipoPatron, name='tipoPatron-eliminar'),
    path('tipoPatron-editar/<int:id>', views.editartipoPatron, name='tipoPatron-editar'),
    path('tipoPatron-actualizar/', views.actualizartipoPatron, name='tipoPatron-actualizar'),
    path('tipoPatron-buscar/', views.buscartipoPatron, name='tipoPatron-buscar'),
    #______________________________________________________________________________________________
    #Compras
    path('compras/', views.listarCompras, name='compras'),
    path('compras-add/', views.insertarCompra, name='compra-add'),
    path('compras-guardar/', views.guardarCompra, name='compra-guardar'),
    path('compras-editar/<int:id>', views.editarCompra, name='compra-editar'),
    path('compras-actualizar/', views.actualizarCompra, name='compra-actualizar'),
    path('compras-buscar/', views.buscarCompra, name='compra-buscar'),
    #______________________________________________________________________________________________
    #Correos
    path('correos/', views.listarCorreos, name='correos'),
    path('correos-add/', views.crearCorreo, name='correos-add'),
    path('correos-guardar/', views.guardarCorreo, name='correos-guardar' ),
    path('correos-editar/<int:id>', views.editarCorreo, name='correos-editar'),
    path('correos-actualizar/', views.actualizarCorreo, name='correos-actualizar'),
    path('correos-buscar/', views.buscarCorreos, name='correos-buscar'),
    path('correos-eliminar/<int:id>', views.eliminarCorreo, name='correos-eliminar'),
]