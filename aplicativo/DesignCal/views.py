from pyexpat.errors import messages
from django.shortcuts import render, redirect
from .models import Factura, Patrone, Rol, TipoPatron, Usuario, Compra, Correos
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from os import remove, path 
BASE_DIR = Path(__file__).resolve().parent.parent
#cifrado de claves
from .crypt import claveEncriptada
#----------------------------------------------------------
#Index
def index(request):
    return render(request, 'DesignCal/index.html')
#----------------------------------------------------------
#Login
def loginFormulario(request):
    return render(request, 'DesignCal/Login/login.html')

def login(request):
    #Capturamos los datos enviados
    if request.method == "POST":
        try:
            u = request.POST["usuario"]
            p = claveEncriptada(request.POST["contrasena"])
            print(p)
            
            #Verificar si existe en la base de datos
            q = Usuario.objects.get(usuario = u, contrasena = p)
            
            #Crear la variable de sesión, aquí interesa guardar quién está logueado, para controlar los permisos
            request.session["logueo"] = [q.cedula, q.nombre, q.apellido, q.NombreRol.NombreRol]
            return redirect('DesignCal:index')
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no existe")
            return redirect('DesignCal:login-formulario')
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:login-formulario')
        
def logout(request):
    try:
        del request.session["logueo"]
        messages.success(request, "Sesión cerrada correctamente")
    except Exception as e:
        messages.error(request, f"Ocurrió un error: {e}")
    return redirect('DesignCal:index')

def perfil(request):
    login = request.session.get('logueo', False)
    q = Usuario.objects.get(pk = login[0])
    contexto = {'perfil': q}
    return render(request, 'DesignCal/Usuarios/perfil.html', contexto)

def actualizarPerfil(request):
    
    if request.method == "POST":
        try:
            login = request.session.get('logueo', False)
            q = Usuario.objects.get(pk = login[0])
            q.nombre = request.POST['nombre']
            q.apellido = request.POST['apellido']
            
            #Control de correo
            if q.correo != request.POST["correo"]:
                try:
                    Usuario.objects.get(correo = request.POST["correo"])
                    raise Exception("Correo ya existe...")
                except Usuario.DoesNotExist:
                    messages.debug(request, "resultado consulta correo: OK")
                    q.correo = request.POST["correo"]
            else:
                q.correo = request.POST["correo"]
            
            #Control de usuario
            if q.usuario != request.POST["usuario"]:
                try:
                    Usuario.objects.get(usuario = request.POST["usuario"])
                    raise Exception("Usuario ya existe...")
                except Usuario.DoesNotExist:
                    messages.debug(request, "resultado consulta usuario: OK")
                    q.usuario = request.POST["usuario"]
            else:
                messages.debug(request, "No hay cambios en el usuario")
                q.usuario = request.POST["usuario"]
            
            if request.POST["contrasena"] != "":   
                q.contrasena = claveEncriptada(request.POST['contrasena'])
            
            q.save()
            #Enviar Correo
            #protocolo de correos electrónicos SMTP save mail transfer protocol.
            from django.core.mail import send_mail
            try:
                send_mail(
                    'Correo de prueba',
                    'Hola, te escribo desde DesignCal para probar el envío de mensajes desde mi projecto formativo en Django',
                    'valeriaye2019@gmail.com',
                    ['valeria1999.40@hotmail.com', 'vbustamante8@misena.edu.co', 'ruizt_3@hotmail.com'],
                    fail_silently=False
                )
                messages.info(request, "Correo enviado")
            except Exception as e:
                messages.error(request, f"Error: {e}")
            login[1] = q.nombre
            login[2] = q.apellido
            request.session["logueo"] = login
            
            messages.success(request, "Perfil actualizado correctamente.")
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no existe")
        except Exception as e:
            messages.error(request, f"error: {e}")
    else:
        messages.warning(request, "Usted no envió datos.")
    
    return redirect('DesignCal:usuario-perfil')

#----------------------------------------------------------
#Patrones
def listarPatron(request):
    q = Patrone.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Patrones/listarPatrones.html', contexto)

def tarjetasPatrones(request):
    q = Patrone.objects.all()
    contexto = {'datos': q}
    return render(request, 'DesignCal/Patrones/tarjetasPatrones.html', contexto)

def insertarPatron(request):
    t = TipoPatron.objects.all()
    a = Usuario.objects.all()
    contexto = {'usuario': a, 'tipoPatron': t}
    return render(request, 'DesignCal/Patrones/cargarPatrones.html', contexto)

def guardarPatron(request):
    try:
        if request.method == "POST":
            if request.FILES:
                fss = FileSystemStorage()
                a = request.FILES["archivo"]
                archivo = fss.save("DesignCal/files/" + a.name, a)
                f = request.FILES["imagen"]
                file = fss.save("DesignCal/fotos/" + f.name, f)
            
            else:
                file = "DesignCal/fotos/default.jpg"

            t = TipoPatron.objects.get(pk = request.POST["tipoPatron"])
            u = Usuario.objects.get(pk = request.POST["usuario"])
            p = Patrone(
                nombreArchivo = request.POST["nombreArchivo"],
                descripcion = request.POST["descripcion"],
                precio = request.POST["precio"],
                archivo = archivo,
                imagen = file,
                usuario = u,
                tipoPatron = t,
            )
            p.save()
            messages.success(request, "Nuevo patrón de moldería agregado")
            return redirect('DesignCal:patron')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:patron')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:patron')

def editarPatron(request, id):
    t = TipoPatron.objects.all()
    u = Usuario.objects.all()
    p = Patrone.objects.get(pk = id)
    contexto = {'datos': p, 'usuario': u, 'tipoPatron': t}
    return render(request, 'DesignCal/Patrones/editarPatrones.html', contexto)

def actualizarPatron(request):
    try:
        if request.method == "POST":
            t = TipoPatron.objects.get(pk = request.POST["tipoPatron"])
            u = Usuario.objects.get(pk = request.POST["usuario"])
            p = Patrone.objects.get(pk = request.POST["id"])
           
            if request.FILES:
                ruta_foto = str(BASE_DIR) + str(p.imagen.url)

                if path.exists(ruta_foto):
                    if p.imagen.url != "/uploads/DesignCal/fotos/default.jpg":
                        remove(ruta_foto)
                else:
                    raise Exception("La imagen no existe o no se encuentra")
                
                fss = FileSystemStorage()
                a = request.FILES["archivo"]
                archivo = fss.save("DesignCal/files/" + a.name, a)
                f = request.FILES["imagen"]
                file = fss.save("DesignCal/fotos/" + f.name, f)

                p.imagen = file
                p.archivo = archivo
            else:
                print("No se seleccionó foto nueva para éste patrón.")

            p.nombreArchivo = request.POST["nombreArchivo"]
            p.descripcion = request.POST["descripcion"]
            p.precio = request.POST["precio"]
            p.usuario = u
            p.tipoPatron = t

            p.save()
            messages.success(request, "Usuario actualizado con éxito")
            return redirect('DesignCal:patron')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:patron')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:patron')

def buscarPatron(request):
    if request.method == "POST":
        q = Patrone.objects.filter(Q(nombreArchivo__icontains = request.POST["dato"]) |
                                   Q(descripcion__icontains = request.POST["dato"]) |
                                   Q(precio__icontains = request.POST["dato"]) |
                                   Q(usuario__usuario__icontains = request.POST["dato"]) |
                                   Q(tipoPatron__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)
        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Patrones/listarPatronesAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:patron')
    
def eliminarPatron(request, id):
    try:
        p = Patrone.objects.get(pk = id)
        ruta_foto = str(BASE_DIR) + str(p.imagen.url)
        if path.exists(ruta_foto):
            if p.imagen.url != "/uploads/DesignCal/fotos/default.jpg":
                remove(ruta_foto)
        else:
            raise Exception("La imágen no existe o no se encuentra.")

        p.delete()
        messages.success(request, "Patrón de moldería eliminado correctamente")
    except Patrone.DoesNotExist:
        messages.error(request, "ERROR: patrón de moldería no existe")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el patrón de moldería: {e}")
    
    return redirect('DesignCal:patron')
#-------------------------------------------------------------------------------
#Usuarios
def listarUsuarios(request):
    q = Usuario.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Usuarios/listarUsuario.html', contexto)

def agregarUsuarios(request):
    a = Rol.objects.all()
    contexto = {'NombreRol': a}
    return render(request, 'DesignCal/Usuarios/ingresarUsuarios.html', contexto)

def guardarUsuario(request):
    try:
        if request.method == "POST":
            if request.FILES:
                fss = FileSystemStorage()
                f = request.FILES["fotoPerfil"]
                file = fss.save("DesignCal/fotosPerfil/" + f.name, f)
            else:
                file = "DesignCal/fotos/default.jpg"

            a = Rol.objects.get(pk = request.POST["NombreRol"])
            q = Usuario(
                cedula = request.POST["cedula"],
                nombre = request.POST["nombre"],
                apellido = request.POST["apellido"],
                correo = request.POST["correo"],
                usuario = request.POST["usuario"],
                contrasena = claveEncriptada(request.POST["contrasena"]),
                fotoPerfil = file,
                NombreRol = a,
            )
            q.save()
            messages.success(request, "Nuevo usuario agregado")
            return redirect('DesignCal:usuario')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:usuario')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:usuario')

def editarUsuario(request, cedula):
    b = Rol.objects.all()
    a = Usuario.objects.get(pk = cedula)
    contexto = {'datos': a, 'NombreRol': b}
    return render(request, 'DesignCal/Usuarios/editarUsuarios.html', contexto)

def actualizarUsuario(request):
    try:
        if request.method == "POST":
            b = Rol.objects.get(pk = request.POST["NombreRol"])
            a = Usuario.objects.get(pk = request.POST["cedula"])
            
            if request.FILES:
                ruta_foto = str(BASE_DIR) + str(a.fotoPerfil.url)
                if path.exists(ruta_foto):
                    if a.fotoPerfil.url != "/uploads/DesignCal/fotosPerfil/default.jpg":
                        remove(ruta_foto)
                else:
                    raise Exception("La foto no existe o no se encuentra")
                
                fss = FileSystemStorage()
                f = request.FILES["fotoPerfil"]
                file = fss.save("DesignCal/fotosPerfil/" + f.name, f)

                a.fotoPerfil = file
            else:
                print("El usuario no seleccionó foto nueva")
            a.nombre = request.POST["nombre"]
            a.apellido = request.POST["apellido"]
            a.correo = request.POST["correo"]
            a.usuario = request.POST["usuario"]
            a.contrasena = claveEncriptada(request.POST["contrasena"])
            a.NombreRol = b

            a.save()
            messages.success(request, "Usuario actualizado con éxito")
            return redirect('DesignCal:usuario')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:usuario')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:usuario')

def buscarUsuario(request):
    if request.method == "POST":
        q = Usuario.objects.filter(Q(cedula__icontains = request.POST["dato"]) |
                                   Q(nombre__icontains = request.POST["dato"]) |
                                   Q(apellido__icontains = request.POST["dato"]) |
                                   Q(correo__icontains = request.POST["dato"]) |
                                   Q(usuario__icontains = request.POST["dato"]) |
                                   Q(NombreRol__NombreRol__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)
        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Usuarios/listarUsuarioAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:usuario')
    
def eliminarUsuario(request, cedula):
    try:
        a = Usuario.objects.get(pk = cedula)
        ruta_foto = str(BASE_DIR) + str(a.fotoPerfil.url)
        if path.exists(ruta_foto):
            if a.fotoPerfil.url != "/uploads/DesignCal/fotosPerfil/default.jpg":
                remove(ruta_foto)
        else:
            raise Exception("La foto no existe o no se encuentra")
       
        a.delete()
        messages.success(request, "Usuario eliminado correctamente.")
    except Usuario.DoesNotExist:
        messages.error(request, "Usuario no existe")
    except Exception as e:
        messages.error(request, f"Error: {e}")
    return redirect("DesignCal:usuario")

#-----------------------------------------------------------------
#Rol
def listarRoles(request):
    q = Rol.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Rol/listarRoles.html', contexto)

def crearRol(request):
    return render(request, 'DesignCal/Rol/crearRol.html')

def guardarRol(request):
    try:
        if request.method == "POST":
            q = Rol(
                NombreRol = request.POST["NombreRol"],
            )
            q.save()
            messages.success(request, "Nuevo Rol agregado")
            return redirect('DesignCal:roles')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:roles')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:roles')

def editarRol(request, id):
    a = Rol.objects.get(pk = id)
    contexto = {'datos': a}
    return render(request, 'DesignCal/Rol/editarRol.html', contexto)

def actualizarRol(request):
    try:
        if request.method == "POST":
            a = Rol.objects.get(pk = request.POST["id"])
            a.NombreRol = request.POST["NombreRol"]

            a.save()
            messages.success(request, "Rol actualizado con éxito")
            return redirect('DesignCal:roles')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:roles')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:roles')

def buscarRol(request):
    if request.method == "POST":
        q = Rol.objects.filter(Q(NombreRol__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)

        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Rol/listarRolesAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:roles')

def eliminarRol(request, id):
    try:
        a = Rol.objects.get(pk = id)
        a.delete()
        messages.success(request, "Rol eliminado correctamente")
    except Patrone.DoesNotExist:
        messages.error(request, "ERROR: rol no existe")
    except Exception as e:
        messages.error(request, f"No se pudo eliminar el rol: {e}")
    
    return redirect('DesignCal:roles')
#----------------------------------------------------------------------------------------------------------------
#Facturas
def listarFacturas(request):
    q = Factura.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Facturas/listarFactura.html', contexto)

def agregarFactura(request):
    a = Patrone.objects.all()
    contexto = {'nombreArchivo': a}
    return render(request, 'DesignCal/Facturas/crearFactura.html', contexto)

def guardarFactura(request):
    try:
        if request.method == "POST":
            a = Patrone.objects.get(pk = request.POST["nombreArchivo"])
            q = Factura(
                nombreArchivo = a,
                cantidad = request.POST["cantidad"],
                total = request.POST["total"],
                fecha = request.POST["fecha"],
            )
            q.save()
            messages.success(request, "Nueva factura agregada con exito")
            return redirect('DesignCal:facturas')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:facturas')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:facturas')

def buscarFactura(request):
    if request.method == "POST":
        q = Factura.objects.filter(Q(nombreArchivo__nombreArchivo__icontains = request.POST["dato"]) |
                                   Q(fecha__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)
        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Facturas/listarFacturaAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:facturas')
#----------------------------------------------------------------------------------------
#Tipos de patrón
def listartipoPatron(request):
    q = TipoPatron.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Tipo_Patron/listarTipoPatron.html', contexto)

def creartipoPatron(request):
    return render(request, 'DesignCal/Tipo_Patron/crearTipoPatron.html')

def guardartipoPatron(request):
    try:
        if request.method == "POST":
            q = TipoPatron(
                tipoPatron = request.POST["tipoPatron"],
                descripcion = request.POST["descripcion"],
            )
            q.save()
            messages.success(request, "Nuevo tipo de patrón agregado")
            return redirect('DesignCal:tipoPatron')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:tipoPatron')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:tipoPatron')

def eliminartipoPatron(request, id):
    try:
        a = TipoPatron.objects.get(pk = id)
        a.delete()
        messages.success(request, "Tipo de patrón eliminado correctamente!.")
    except TipoPatron.DoesNotExist:
        messages.error(request, "ERROR: tipo de patrón no existe")
    except Exception as e:
        messages.error(request, f'No se pudo eliminar el tipo de patrón: {e}')
        
    return redirect('DesignCal:tipoPatron')

def editartipoPatron(request, id):
    a = TipoPatron.objects.get(pk = id)
    contexto = {'datos': a}
    return render(request, 'DesignCal/Tipo_Patron/editarTipoPatron.html', contexto)

def actualizartipoPatron(request):
    try:
        if request.method == "POST":
            a = TipoPatron.objects.get(pk = request.POST["id"])
            a.tipoPatron = request.POST["tipoPatron"]
            a.descripcion = request.POST["descripcion"]

            a.save()
            messages.success(request, "Tipo de patrón actualizado con éxito")
            return redirect('DesignCal:tipoPatron')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:tipoPatron')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:tipoPatron')

def buscartipoPatron(request):
    if request.method == "POST":
        q = TipoPatron.objects.filter(Q(tipoPatron__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)

        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Tipo_Patron/listarTipoPatronAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:tipoPatron')
#--------------------------------------------------------------------------------------------
#Compras
def listarCompras(request):
    q = Compra.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Compras/listarCompras.html', contexto)

def insertarCompra(request):
    t = Factura.objects.all()
    a = Usuario.objects.all()
    contexto = {'usuario': a, 'IdFactura': t}
    return render(request, 'DesignCal/Compras/crearCompra.html', contexto)

def guardarCompra(request):
    try:
        if request.method == "POST":
            t = Factura.objects.get(pk = request.POST["IdFactura"])
            a = Usuario.objects.get(pk = request.POST["usuario"])
            p = Compra(
                IdFactura = t,
                usuario = a,
                descripcion = request.POST["descripcion"],
                estado = request.POST["estado"]
            )
            p.save()
            messages.success(request, "Nueva compra agregada")
            return redirect('DesignCal:compras')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:compras')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:compras')

def editarCompra(request, id):
    b = Factura.objects.all()
    c = Usuario.objects.all()
    a = Compra.objects.get(pk = id)
    contexto = {'datos': a, 'IdFactura': b, 'usuario': c}
    return render(request, 'DesignCal/Compras/editarCompras.html', contexto)

def actualizarCompra(request):
    try:
        if request.method == "POST":
            b = Factura.objects.get(pk = request.POST["IdFactura"])
            c = Usuario.objects.get(pk = request.POST["usuario"])
            a = Compra.objects.get(pk = request.POST["id"])
            a.IdFactura = b
            a.usuario = c
            a.descripcion = request.POST["descripcion"]
            a.estado = request.POST["estado"]

            a.save()
            messages.success(request, "Compra actualizada con éxito")
            return redirect('DesignCal:compras')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:compras')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:compras')

def buscarCompra(request):
    if request.method == "POST":
        q = Compra.objects.filter(Q(IdFactura__IdFactura__icontains = request.POST["dato"]) |
                                  Q(usuario__usuario__icontains = request.POST["dato"]) |
                                  Q(estado__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)
        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Compras/listarComprasAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:compras')

#-----------------------------------------------------------------------------------------
#Correos

def listarCorreos(request):
    q = Correos.objects.all()
    pag = Paginator(q, 5)
    page_number = request.GET.get('page')
    q = pag.get_page(page_number)
    contexto = {'datos': q}
    return render(request, 'DesignCal/Correos/listarCorreos.html', contexto)

def crearCorreo(request):
    u = Usuario.objects.all()
    contexto = {'usuario': u}
    return render(request, 'DesignCal/Correos/crearCorreos.html', contexto)

def guardarCorreo(request):
    try:
        if request.method == "POST":
            u = Usuario.objects.get(pk = request.POST["usuario"])
            q = Correos(
                usuario = u,
                titulo = request.POST["titulo"],
                contenido = request.POST["contenido"],
            )
            q.save()
            messages.success(request, "Nueva correo agregado con exito")
            return redirect('DesignCal:correos')
        else:
            messages.warning(request, "Usted no envió datos")
            return redirect('DesignCal:correos')
    except Exception as e:
        messages.error(request, 'Error: ' + str(e))
        return redirect('DesignCal:correos')

def eliminarCorreo(request, id):
    try:
        a = Correos.objects.get(pk = id)
        a.delete()
        messages.success(request, "Correo eliminado correctamente!.")
    except Correos.DoesNotExist:
        messages.error(request, "ERROR: correo no existe")
    except Exception as e:
        messages.error(request, f'No se pudo eliminar el correo: {e}')
        
    return redirect('DesignCal:correos')

def editarCorreo(request, id):
    a = Correos.objects.get(pk = id)
    u = Usuario.objects.all()
    contexto = {'datos': a, 'usuario': u}
    return render(request, 'DesignCal/Correos/editarCorreos.html', contexto)

def actualizarCorreo(request):
    try:
        if request.method == "POST":
            u = Usuario.objects.get(pk = request.POST["usuario"])
            c = Correos.objects.get(pk = request.POST["id"])
            c.usuario = u,
            c.titulo = request.POST["titulo"]
            c.contenido = request.POST["contenido"]

            c.save()
            messages.success(request, "Correo actualizado con éxito")
            return redirect('DesignCal:correos')
        else:
            messages.warning(request, "No hay cambios")
            return redirect('DesignCal:correos')
    except Exception as e:
        messages.error(request, "Error: " + str(e))
        return redirect('DesignCal:correos')

def buscarCorreos(request):
    if request.method == "POST":
        q = Correos.objects.filter(Q(usuario__usuario__icontains = request.POST["dato"]) |
                                   Q(titulo__icontains = request.POST["dato"]))
        pag = Paginator(q, 5)
        page_number = request.GET.get('page')
        q = pag.get_page(page_number)
        contexto = {'datos': q, 'datoBuscado': request.POST["dato"]}
        return render(request, 'DesignCal/Correos/listarCorreosAjax.html', contexto)
    else:
        messages.warning(request, "Usted no envió datos...")
        return redirect('DesignCal:correos')
    

