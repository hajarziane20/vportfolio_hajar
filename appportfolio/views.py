# -*- coding: utf-8 -*- 
from __future__ import unicode_literals

from lib2to3.fixes.fix_input import context

from django.shortcuts import render,redirect,get_object_or_404
from contextlib import redirect_stderr
from django.http import HttpResponse 
from appportfolio.models import * #importamos los modelos.
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger	#paginacion
#fichero cuyos print aparecen en consola, es el archivo controlador
from django.contrib.auth.decorators import login_required
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User #contrib=permisos,usuarios,roles... de todos los nmodelos importamos User
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.views.decorators.csrf import csrf_protect
import urllib #para saber las ip's conectadas
from django.conf import settings
'''
def home(request): 
    cadena='<center><b>Inicio!</b></center>'
    return HttpResponse(cadena)
'''
def home(request):
    print("hola estoy en Home ")
    nombreProyecto='PORTfolio'
    fechaCreacion='23/09/2024'
    #AÑADIDO DE IP
    actual=request.user
    idusuario=0
    idusuario=actual.id
    request.session['idusuario']=idusuario
    numconetados=0
    dato=""
    #ip externa o publica
    lista="0123456789"
    ip=""
    try:
        dato = urllib.request.urlopen('https://www.wikipedia.org').headers['X-Client-IP']  # 7/9/2024 va muy bien
        # dato = urllib.request.urlopen('https://ident.me').read().decode('utf8')  # python 3 este es bueno desde 28/7/2021
        # dato = urllib.urlopen('https://ident.me').read().decode('utf8')  # python 3 este es el bueno 28/7/2021
        print("IP PUBLICA=" + str(dato))
    except:
        print("Error en la Librería de la IP ")
        # dato = urllib.urlopen('https://ident.me').read()
        # dato = urllib.request.urlopen('https://ident.me').read()  # python 3 el guay 28/7/2021
        # dato = urllib.urlopen('http://checkip.dyndns.org').read()  # ojo hasta 28/7/2021 usada siempre da error
        dato = ""
    finally:
        print("USUARIO ACTUAL.... [" + str(actual) + "]")

    for x in str(dato):
        if x in lista:
            ip += x
    if str(actual) == "AnonymousUser":
        request.session['tipousuario'] = 'anonimo'
        print("IP ANONIMO...." + str(ip))
        # GUARDAMOS EL EVENTO DE LA IP DEL USUARIO ANONIMO
        '''
        anonimo = Anonimo()
        anonimo.fecha = timezone.now()
        anonimo.entra = timezone.now()
        anonimo.ip = ip
        anonimo.save()
        '''
        usuario = 'prueba'

    context= {'nombreProyecto':nombreProyecto, 'fechaCreacion':fechaCreacion} #creamos un contexto de compartición. Le enviamos la pareja 'variable valor' formato json. En python esa estructura se llama diccionario.
    return render(request, 'home.html', context=context) #hago una petición, página a la que hago request y las variables en el contexto que envio a esa pag

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)#no me registro si no que entro me logueo, me busca en la tabla
        if user is not None: #if not null = existe
            login(request, user)

            actual=request.user #coge el usuario actual
            idusuario=0  #incializar a 0
            idusuario=actual.id #sobre el actual cogemos su id. (de user no de netrevistador)
            request.session['idusuario']=idusuario
            print('idusuario=' + str(idusuario))
            entrevistador=Entrevistador.objects.get(user=idusuario) #user es la foreign key se contraresta con el id del actual.
            idEntrevistador=entrevistador.id #una vez tenemos un el entrev, cogemos su id, si fuera filter con muchos registros tendría que recorrer el record.
            print('idEntrevistador=' + str(idEntrevistador))
            print("FOTO="+str(entrevistador.avatar))
            fotoperfil=settings.MEDIA_URL+str(entrevistador.avatar) if entrevistador.avatar else settings.MEDIA_URL+"logo.png"
                #si pongo 'media/' en vez de settings.MEDIA_URL  no lo coge, error porq la va a buscar como url de página.
                #MEDIA_URL en settings.py define la segunda caparpeta media.
                #avatar es un campo del modelo entrevistador.
                #else es como una foto por defecto
            print("avatar="+str(fotoperfil))
            context={'fotoperfil':fotoperfil}#para q pinte la imagen en home.
            return render(request,'home.html',context=context)#cambio redirect por render al pasar el contexto.
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'}) #error pasado por contexto.
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username'] #otra forma de request.POST.get('empresa') (se puede hacer de las 2 formas)
        password = request.POST['password']
        user = User.objects.create_user(username=username, password=password) #objeto user, recibe del modelo User el insert into(create_user)
        user.save()
        return redirect('login')  # Redirige al login una vez registrado(cuando salgo)
    return render(request, 'register.html') #cuando entro,es el get

# CERRAR LA SESION DEL USUARIO
def cerrar(request):
    username = request.user.username
    password = request.user.password
    idusuario = request.user.id
    print("logout.............." + username + " clave=" + str(password) + " id=" + str(idusuario))
    user = authenticate(request, username=username, password=password)
    # desconectamos al usuario
    logout(request)
    return redirect('/')


def sobremi(request):
    print("hola estoy en Sobre Mi")
    nombre='Hajar'
    edad=20
    telefono='633456782'
    cargo='Admin'
    ListaCategorias=Categoria.objects.all().order_by('-id') #selet * from Categoria
    for r in ListaCategorias:
        print(str(r.nombre_categoria))

    context= {'nombre':nombre, 'edad':edad, 'telefono':telefono, 'cargo':cargo
              , 'ListaCategorias':ListaCategorias}
    return render(request, 'sobremi.html', context=context)

'''##################################################
#                   HABILIDAD                       #
##################################################'''
def habilidades(request):
    print("hola estoy en Habilidades")
    #de la tabla Habilidad quiero todos los objetos (select* order by habilidad)
    #habilidades=Habilidad.object.all().order_by('habilidad') #si no le pongo nada es ascendente y si lepongo '-habilidad' descendiente.
    #habilidades es un objeto de tipo queryset

    lista_habilidades = Habilidad.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(lista_habilidades, 5)
    if page == None:
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages
        request.session[
            "pagina"] = page
    else:
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page

    if request.method == 'GET':
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session:
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_habilidades = paginator.get_page(page)
    except PageNotAnInteger:
        lista_habilidades = paginator.page(1)
    except EmptyPage:
        lista_habilidades = paginator.page(paginator.num_pages)

    context={'lista_habilidades':lista_habilidades}
    return render(request, 'habilidades.html', context=context)

def ver_habilidad(request,id): #primero request y luego id(sino error)
    expe_id=id #recibe el id al que le he dado.
    habilidad = Habilidad.objects.get(id=expe_id)
    context = {'habilidad': habilidad}  #pasamos el queryset
    return render(request, 'ver_habilidad.html',context=context) #con esa request, llamamo a ver_exp y le pasamos el context.

def eliminar_habilidad(request,pkHab):
    print("Eliminar")
    exp_id=pkHab
    habilidad= Habilidad.objects.get(id=exp_id)
    if request.method == 'POST':
        habilidad.delete()
        return redirect('habilidades') #daba error el redirect. causa: no está importado.
    return render(request, 'eliminar_habilidad.html', {'habilidad':habilidad})

'''##################################################
#                   CATEGORIA                       #
##################################################'''
def categorias(request):
    #Obtener un objeto queryset del modelo de categorias
    lista_categorias = Categoria.objects.all()  # select * from Categoria;
    page = request.GET.get('page') #cuando entro a la página, linea obligatoria, es lo que paginamos
    #Registros por pagina.
    paginator = Paginator(lista_categorias, 5)  # 5 registros(items) por página (de 5 en 5)
    if page == None: #al entrar todavia no he pulsado ninguna pág
        print(" page recibe fuera de get o post NONE=" + str(page))
        page = paginator.num_pages #numero de página calculado por paginator (si los divido en 5 tendré 3 pag (5+5+2)
        request.session["pagina"] = page #variablede sesión: vale para todas las páginas de todo el proyecto.Ej: soy hajar en todas las vistas de una red social.
    else: #cuando pulse 1 coge 1 y asi con los demás paginas.
        print(" page recibe esle del none de geo o post=" + str(page))
        request.session["pagina"] = page #pagina: nombre variable, page:valor.

    if request.method == 'GET': #entrada a la página
        pagina = request.session["pagina"]
        print(" page recibe en GET=" + str(pagina))
    if request.method == 'POST':#salida de la página
        pagina = request.session["pagina"]
        print(" page recibe en POST=" + str(pagina))

    if "pagina" in request.session: #verificar si existe la variable (es por si se ha borrado en algúna parte)
        page = request.session["pagina"]
        print(" page recibe de sesion=" + str(page))

    try:
        lista_categorias = paginator.get_page(page)
    except PageNotAnInteger: #en caso de que no reciba un int lo pone a 1
        lista_categorias = paginator.page(1)
    except EmptyPage:
        lista_categorias = paginator.page(paginator.num_pages)

    context = {'lista_categorias': lista_categorias} #definimos variable:valor.
    return render(request, 'categorias.html', context=context)

'''##################################################
#                    ESTUDIOS                       #
##################################################'''
def estudios(request):
    # Obtener un objeto queryset del modelo de categorias
    lista_estudios = Estudio.objects.all().order_by("id")  # select * from Categoria;
    page = request.GET.get('page')  # Capturar el número de página de la URL (por ejemplo: ?page=2)

    # Configurar la paginación con 2 registros por página
    paginator = Paginator(lista_estudios, 2)

    try:
        # Obtener la página solicitada por el usuario
        lista_estudios = paginator.get_page(page)
    except PageNotAnInteger:
        # Si el número de página no es un entero, mostrar la primera página
        lista_estudios = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        lista_estudios = paginator.page(paginator.num_pages)
    numregistros=Estudio.objects.count()
    # Definir el contexto y renderizar la plantilla
    context = {'lista_estudios': lista_estudios, "numregistros":numregistros}
    return render(request, 'estudios.html', context=context)

'''##################################################
#                   EXPERIENCIA                     #
##################################################'''

def experiencias(request):
    # Obtener un objeto queryset del modelo de categorias
    lista_experiencias = Experiencia.objects.all().order_by("id")  # select * from Categoria;
    page = request.GET.get('page')  # Capturar el número de página de la URL (por ejemplo: ?page=2)

    # Configurar la paginación con 2 registros por página
    paginator = Paginator(lista_experiencias, 2)

    try:
        # Obtener la página solicitada por el usuario
        lista_experiencias = paginator.get_page(page)
    except PageNotAnInteger:
        # Si el número de página no es un entero, mostrar la primera página
        lista_experiencias = paginator.page(1)
    except EmptyPage:
        # Si el número de página está fuera de rango, mostrar la última página
        lista_experiencias = paginator.page(paginator.num_pages)
    numregistros=Experiencia.objects.count()
    # Definir el contexto y renderizar la plantilla
    context = {'lista_experiencias': lista_experiencias, "numregistros":numregistros}
    return render(request, 'experiencias.html', context=context)

def ver_experiencia(request,id): #primero request y luego id(sino error)
    expe_id=id #recibe el id al que le he dado.
    experiencia = Experiencia.objects.get(id=expe_id)
    context = {'experiencia': experiencia}  #pasamos el queryset
    return render(request, 'ver_experiencia.html',context=context) #con esa request, llamamo a ver_exp y le pasamos el context.

def eliminar_experiencia(request,pk):
    print("Eliminar")
    exp_id=pk
    experiencia= Experiencia.objects.get(id=exp_id)
    if request.method == 'POST':
        experiencia.delete()
        return redirect('experiencias') #daba error el redirect. causa: no está importado.
    return render(request, 'eliminar_experiencia.html', {'experiencia':experiencia})

def crear_experiencia(request):
    if request.method == 'POST': #si en el request el  méto do que viene es post
        empresa = request.POST.get('empresa')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')
        observaciones = request.POST.get('observaciones')
        categoria = request.POST.get('categoria')

        experiencia=Experiencia();
        experiencia.empresa=empresa
        experiencia.fecha_inicio=fecha_inicio
        experiencia.fecha_fin=fecha_fin
        experiencia.observaciones=observaciones
        experiencia.categoria=categoria
        experiencia.save()
        return redirect('experiencias')  # Redirige  a otra página

    return render(request, 'crear_experiencia.html')

def editar_experiencia(request, experiencia_id):
    experiencia = Experiencia.objects.get(id=experiencia_id)

    if request.method == 'POST':
        experiencia.empresa =  request.POST.get('empresa')
        experiencia.fecha_inicio = request.POST.get('fecha_inicio')
        experiencia.fecha_fin = request.POST.get('fecha_fin')
        experiencia.observaciones = request.POST.get('observaciones')
        experiencia.categoria = request.POST.get('categoria')
        experiencia.save() #este no hace un Personal() porq no es nuevo sino existente.
        return redirect('experiencias')  # Redirige a la lista de personas o a otra página

    return render(request, 'editar_experiencia.html', {'experiencia': experiencia})

def entrevistadores(request):
   titulo="Gestión de entrevistas"
   context={'titulo':titulo}
   return render(request, 'entrevistadores.html',context=context)
'''##################################################
#                     IMÁGENES                     #
##################################################'''

def subir_imagenes(request):
    #idUsuario=request.session['idusuario']
    if request.method == 'POST':
        imagenes=request.FILES.getlist('imagenes')

        for imagen in imagenes:
            if imagen.name.endswith(('.jpg','png','jpeg','.gif','.jfif')):
                img=Imagen()
                img.imagen=imagen
                img.save()
        return redirect('subir_imagenes')
    imagenes=Imagen.objects.all()
    return render(request, 'subir_imagenes.html',{'imagenes':imagenes})

def editar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    if request.method == 'POST' and request.FILES.get('nueva_imagen'):
        # Actualizamos la imagen
        imagen.imagen = request.FILES['nueva_imagen']
        imagen.imagen = request.FILES['nueva_imagen']
        imagen.save()
        return redirect('subir_imagenes')  # Redirige a la galería de imágenes
    return redirect('subir_imagenes')

def eliminar_imagen(request, imagen_id):
    imagen = get_object_or_404(Imagen, id=imagen_id)
    if request.method == 'POST':
        imagen.delete()
        return redirect('subir_imagenes')  # Redirige a la galería de imágenes
    return redirect('subir_imagenes')

def subir_videos(request):
    if request.method == 'POST' and request.FILES['videos']:
        videos=request.FILES.getlist('videos')

        for video in videos:
            if video.name.endswith(('.mp4','.avi','.mp3','.mov','.mkv')):
                v=Video()
                v.video=video
                v.save()

        return redirect('subir_videos')
    videos=Video.objects.all()
    return render(request, 'subir_videos.html',{'videos':videos})

def editar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST' and request.FILES.get('nuevo_video'):
        # Actualizamos el video
        video.video = request.FILES['nuevo_video']
        video.save()
        return redirect('subir_videos')
    return redirect('subir_videos')

def eliminar_video(request, video_id):
    video = get_object_or_404(Video, id=video_id)
    if request.method == 'POST':
        print("BORRAMOS VIDEO")
        video.delete()
        return redirect('subir_videos')
    return redirect('subir_videos')





















