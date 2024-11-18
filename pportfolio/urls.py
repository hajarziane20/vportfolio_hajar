# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from tkinter.font import names

from django.contrib import admin
#las 3 formas según las versiones, usamos re_path que es el último
from django.urls import path, include, re_path
from appportfolio import views
from appportfolio.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),  
    path('',views.home,name='home'),
    path('sobremi/',views.sobremi,name='sobremi'),
    re_path('categorias/',views.categorias,name='categorias'),
    re_path('habilidades/',views.habilidades,name='habilidades'),
    re_path('estudios/', views.estudios, name='estudios'),
    re_path('experiencias/', views.experiencias, name='experiencias'),
    re_path(r'^(?P<id>\d+)/ver_experiencia$', views.ver_experiencia,name='ver_experiencia'),
    #r(regular expression formada por un inicio y un final)
    #’’ contenido de exp
    #^inicio de expReg
    #?P patrón que coge los char (para que coja un nombre tamb y lo ponga en la url
    #<id> va a recibir un id
    #\d tipo integer
    #+ permite cualquier cifra (si solo pongo d solo permite un num)
    #$ cierre de expReg.
    #re_path('ver_experiencias/<int:id>/',vieviews.ver_experiencia,name='ver_experiencia'), Otra forma (formato amigable)
    path('eliminar_experiencia/<int:pk>/', views.eliminar_experiencia,name='eliminar_experiencia'),
    #int pk recibe el id de eliminar_experiencia.html
    path('ver_habilidad/<int:id>/', views.ver_habilidad,name='ver_habilidad'),#DUDA
    path('eliminar_habilidad/<int:pkHab>/', views.eliminar_habilidad,name='eliminar_habilidad'),
    path('experiencia/nueva/', views.crear_experiencia, name='crear_experiencia'),
    path('experiencia/editar/<int:experiencia_id>/', views.editar_experiencia, name='editar_experiencia'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('cerrar/',views.cerrar, name="cerrar"),
    path('entrevistadores',views.entrevistadores, name='entrevistadores'),
    path('subir_imagenes/',views.subir_imagenes,name='subir_imagenes'),
    path('subir_videos/',views.subir_videos,name='subir_videos'),
    path('imagen/editar/<int:imagen_id>/', views.editar_imagen, name='editar_imagen'),
    path('imagen/eliminar/<int:imagen_id>/',views.eliminar_imagen, name='eliminar_imagen'),
    path('video/editar/<int:video_id>/', views.editar_video, name='editar_video'),
    path('video/eliminar/<int:video_id>/', views.eliminar_video, name='eliminar_video'),
    path('contacto/', views.contacto, name='contacto'),
    path('generar_pdf/<int:entrevistador_id>/',views.generar_pdf,name='generar_pdf'),
    path('listar_entrevistadores/', views.listar_entrevistadores, name='listar_entrevistadores'),
    path('crear_curriculum/', views.crear_curriculum, name='crear_curriculum'),
    path('pintar_curriculum/<int:pkcur>/', views.pintar_curriculum, name='pintar_curriculum'),
    path('generar_curriculum/<int:pkcur>/', views.generar_curriculum, name='generar_curriculum'),
    path('lista_noticias', views.lista_noticias, name='lista_noticias'),
    path('crear_noticia', views.crear_noticia, name='crear_noticia'),

]




#ulrpatters: es una estructura en la que metemos items, se trata de patrones de mapeo, por eso el nombre,

#Abrimos otro urlpatterns porque una cosa es el mapping normal, y otra el tratamiento de los ficheros estáticos
urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns+=static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns+=[
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),#primer media, y a partir de ahi reconece todas las subcarpetas.
]























