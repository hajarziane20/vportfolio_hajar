# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# Importaciones de Django
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger  # Paginación
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.conf import settings

# Importaciones adicionales
from appportfolio.models import *  # Importación de modelos
from contextlib import redirect_stderr
import os  # Para el sistema de archivos
import urllib  # Para obtener IPs conectadas
from tempfile import template  # Plantillas temporales
from lib2to3.fixes.fix_input import context  # Contexto para plantillas

# Importaciones de ReportLab
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader

'''##################################################
#                     INICIO                       #
##################################################'''
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
#                USUARIO-SESIÓN                    #
##################################################'''
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)#no me registro si no que entro me logueo, me busca en la tabla
        if user is not None: #if not null = existe
            login(request,user)
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


'''##################################################
#                     MULTIMEDIA                     #
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

'''##################################################
#                     CONTACTO(email)                #
##################################################'''
def contacto(request):
    if request.method == "POST":
        nombre = request.POST.get('nombre')
        user_email = request.POST.get('email')  # Cambié 'email' a 'user_email'
        asunto = request.POST.get('asunto')
        mensaje = request.POST.get('mensaje')

        context = {'nombre': nombre, 'email': user_email, 'asunto': asunto, 'mensaje': mensaje}
        template = render_to_string('email_template.html', context=context)

        # Yo soy el emisor y el email indicado el receptor.
        '''email_message = EmailMessage(
            asunto,
            template,
            settings.EMAIL_HOST_USER,
            ['zianef45@gmail.com']
        )'''
        # Yo soy el receptor y el usuario el emisor
        email_message = EmailMessage(
            asunto,
            template,
            user_email,
            ['hajar.ziane.5@gmail.com']
        )

        email_message.fail_silently = False  # Que no marque error en Gmail
        email_message.send()

        messages.success(request, 'Se ha enviado tu email')
        return redirect('home')

    return render(request, 'correo.html')

'''##################################################
#             PDF/ENTREVISTADOR                      #
##################################################'''
def entrevistadores(request):
   titulo="Gestión de entrevistas"
   context={'titulo':titulo}
   return render(request, 'entrevistadores.html',context=context)

def listar_entrevistadores(request):
    entrevistadores= Entrevistador.objects.all()
    return render(request,'listar_entrevistadores.html',{'entrevistadores':entrevistadores})

def generar_pdf(request, entrevistador_id):
    entrevistador=Entrevistador.objects.get(id=entrevistador_id)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="entrevistadores{entrevistador.id}.pdf"'

    p=canvas.Canvas(response, pagesize=letter)

    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.darkblue)
    p.drawCentredString(300,770, "Reporte de entrevistador")

    p.setFont("Helvetica-Bold", 16)
    p.setFillColor(colors.burlywood)

    p.drawString(100,720,f"ID:{entrevistador.id}")#concatena
    p.drawString(100, 700, f"Empresa:{entrevistador.empresa or 'N/A'}")
    p.drawString(100, 680, f"Fecha de Entrevista:{entrevistador.fecha_entrevista or 'N/A'}")
    p.drawString(100, 660, f"Conectado:{entrevistador.conectado or 'N/A'}")
    p.drawString(100, 640, f"Seleccionado:{entrevistador.seleccionado or 'N/A'}")
    p.drawString(100, 620, f"Usuario:{entrevistador.user.username if entrevistador.user else 'N/A'}")

    #la imagen, puede ser que no tenga imagen.
    if entrevistador.avatar:
        avatar_path=entrevistador.avatar.path
        p.drawImage(avatar_path, 100, 500,width=100, height=100)

    p.showPage()
    p.save()

    return response



def crear_curriculum(request):
    persona=Personal.objects.get(id=1)
    if request.method == 'POST':
        id=persona.id;
        nombre=persona.nombre;
        ap1=persona.apellido1;
        ap2=persona.apellido2;

        email = request.POST.get('email')
        telefono = request.POST.get('telefono')

        curriculum = Curriculum();
        curriculum.id = id
        curriculum.nombre=nombre
        curriculum.ap1=ap1
        curriculum.ap2=ap2
        curriculum.email=email
        curriculum.telefono=telefono
        curriculum.save()
        return redirect('pintar_curriculum', pk=curriculum.pk)

    return render(request, 'crear_curriculum.html')


def pintar_curriculum(request, pkcur):
    curriculum = get_object_or_404(Curriculum, id=pkcur)
    estudios = DetalleCurriculumEstudio.objects.filter(fk_Curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(fk_Curriculum=curriculum)

    context = {'curriculum': curriculum, 'estudios': estudios, 'experiencias': experiencias, 'pkcur': pkcur}
    return render(request, 'curriculum.html', context=context)




def generar_curriculum(request, pkcur):
    curriculum = get_object_or_404(Curriculum, id=pkcur)
    estudios = DetalleCurriculumEstudio.objects.filter(fk_Curriculum=curriculum)
    experiencias = DetalleCurriculumExperiencia.objects.filter(fk_Curriculum=curriculum)

    # Crear la respuesta HttpResponse con tipo de contenido PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="curriculum_{curriculum.nombre}_{curriculum.ap1}.pdf"'

    # Crear un objeto canvas de ReportLab para generar el PDF
    c = canvas.Canvas(response, pagesize=letter)
    width, height = letter  # Tamaño de la página

    # Establecer la paleta de colores
    color_principal = "#771011"
    color_secundario = "#d1d1d1"

    # Cargar imagen de avatar
    try:
        avatar_path = os.path.join(settings.MEDIA_ROOT, "media/HJ.jpg")
        avatar = ImageReader(avatar_path)
        c.drawImage(avatar, width - 150, height - 150, width=100, height=100)
    except Exception as e:
        print(f"No se pudo cargar la imagen: {e}")
        pass  # Si no se encuentra la imagen, el PDF se generará sin ella

    # Título del currículum en color principal
    c.setFont("Helvetica-Bold", 22)
    c.setFillColor(colors.HexColor(color_principal))  # Usamos el color principal
    c.drawString(100, height - 100, f"Curriculum de {curriculum.nombre} {curriculum.ap1}")

    # Información de contacto en color secundario
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(100, height - 130, f"Email: {curriculum.email}")
    c.drawString(100, height - 150, f"Teléfono: {curriculum.telefono}")

    # Sección de estudios en color secundario
    y_position = height - 200
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor(color_principal))  # Color principal
    c.drawString(100, y_position, "Estudios:")

    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    for estudio in estudios:
        c.drawString(100, y_position, f"{estudio.fk_Detalle_Estudio.titulo} en {estudio.fk_Detalle_Estudio.ciudad} ({estudio.fk_Detalle_Estudio.fechaInicio} - {estudio.fk_Detalle_Estudio.fechaFin})")
        y_position -= 20

    # Sección de experiencia laboral
    y_position -= 40
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor(color_principal))  # Color principal
    c.drawString(100, y_position, "Experiencia laboral:")

    y_position -= 20
    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    for experiencia in experiencias:
        c.drawString(100, y_position, f"{experiencia.fk_Detalle_Experiencia.categoria} en {experiencia.fk_Detalle_Experiencia.empresa} ({experiencia.fk_Detalle_Experiencia.fecha_inicio} - {experiencia.fk_Detalle_Experiencia.fecha_fin})")
        y_position -= 20

    # Agregar un espacio al final
    y_position -= 40
    c.setFillColor(colors.HexColor(color_secundario))  # Color secundario
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(100, y_position, f"Generado con orgullo para {curriculum.nombre} {curriculum.ap1}")

    # Finalizar el PDF
    c.showPage()  # Si tienes más páginas
    c.save()

    return response

def lista_noticias(request):
    noticias=Noticia.objects.all().order_by('-fecha_creacion')
    return render(request,'lista_noticias.html',{'noticias':noticias})

def crear_noticia(request):
    if request.method == "POST":
        titulo = request.POST.get('titulo')
        contenido = request.POST.get('contenido')
        imagen = request.FILES.get('imagen')

        if titulo and contenido:
            noticia=Noticia.objects.create(titulo=titulo, contenido=contenido, imagen=imagen)
            return redirect(lista_noticias)
        else:
            return HttpResponse("Error: El titulo y el contenido son obligatorios", status=400)
    return  render(request,'crear_noticia.html')


def list_valoraciones(request):
    valoraciones=Valoracion.objects.all()
    return render(request,'list_valoraciones.html', {'valoraciones':valoraciones})

def actualizar_valoracion(request,pk):
    valoracion=get_object_or_404(Valoracion, pk=pk)
    if request.method == "POST":
        votos_entrevista=int(request.POST.get('votos_entrevista', valoracion.votos_entrevista))
        votos_empresa=int(request.POST.get('votos_empresa', valoracion.votos_empresa))

        #Actualizar los votos y recalcular la media.
        valoracion.votos_entrevista=votos_entrevista
        valoracion.votos_empresa=votos_empresa
        valoracion.media_aspectos=(votos_entrevista + votos_empresa) / 2
        valoracion.save()

        return redirect('list_valoraciones')
    return render(request,'update_valoracion.html', {'valoracion':valoracion})



def añadir_valoracion(request):
    if request.method == "POST":
        entrevista=request.POST.get('entrevista')
        empresa=request.POST.get('empresa')
        votos_entrevista=int(request.POST.get('votos_entrevista', 0))
        votos_empresa=int(request.POST.get('votos_empresa', 0))

        #Calcular la media de los apespectos
        media_aspectos = (votos_entrevista + votos_empresa) / 2

        #Crear y guardar la nueva valoración.
        nueva_valoracion=Valoracion.objects.create(
            entrevista=entrevista,
            empresa=empresa,
            votos_entrevista=votos_entrevista,
            votos_empresa=votos_empresa,
            media_aspectos=media_aspectos
        )
        return redirect('listar_valoraciones')
    return render(request, 'add_valoracion.html')





















































