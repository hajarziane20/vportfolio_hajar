# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from dataclasses import field

from django.contrib import admin
from appportfolio.models import *
from django.contrib.auth.models import User 


admin.site.site_header = "Sitio web Salmantino"  #este es el título
admin.site.site_title = "Portal de Portfolio"
admin.site.index_title = "Bienvenidos al portal de Administración"


class HabilidadAdmin(admin.ModelAdmin):
    list_display = [co.name for co in Habilidad._meta.get_fields()] 
    search_fields = ('id','habilidad','nivel') #siempre tienen que ser una tupla
    list_filter   = ('id','habilidad','nivel') #siempre tienen que ser una tupla
admin.site.register(Habilidad, HabilidadAdmin)

class PersonalAdmin(admin.ModelAdmin):
    list_display = [co.name for co in Personal._meta.get_fields()] 
    search_fields = ('id','nombre','apellido1','apellido2','edad') 
    list_filter   = ('id','nombre','apellido1','apellido2','edad') 
admin.site.register(Personal, PersonalAdmin)

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['id','nombre_categoria']
    search_fields = ('id','nombre_categoria')
    list_filter   = ('id','nombre_categoria')
admin.site.register(Categoria, CategoriaAdmin)

class EstudioAdmin(admin.ModelAdmin):
    list_display = ['id','titulo',"fechaInicio","fechaFin","notamedia","nombreLugar","nombreLugar","ciudad","presencial","observaciones"]
    search_fields = ('id','titulo',"fechaInicio","fechaFin","notamedia","nombreLugar","nombreLugar","ciudad","presencial","observaciones")
    list_filter   = ('id','titulo',"fechaInicio","fechaFin","notamedia","nombreLugar","nombreLugar","ciudad","presencial","observaciones")
admin.site.register(Estudio, EstudioAdmin)

class ExperienciaAdmin(admin.ModelAdmin):
    list_display = ['id','empresa',"fecha_inicio","fecha_fin","observaciones","categoria"]
    search_fields = ('id','empresa',"fecha_inicio","fecha_fin","observaciones","categoria")
    list_filter   = ('id','empresa',"fecha_inicio","fecha_fin","observaciones","categoria")
admin.site.register(Experiencia, ExperienciaAdmin)
''''''
class ImagenAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Imagen._meta.get_fields() if hasattr(field, 'verbose_name')]
    search_fields = ('id','imagen')
    list_filter   = ('id','imagen')
admin.site.register(Imagen, ImagenAdmin)
#Error aquí: puse class Imagen y abajo puse ImagenAdmin, cuanod deben llamarse igual.

class VideoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Video._meta.get_fields() if hasattr(field, 'verbose_name')]
    search_fields = ('id','video')
admin.site.register(Video, VideoAdmin)

class EntrevistadorAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Entrevistador._meta.get_fields() if hasattr(field, 'verbose_name')] #es una lista, siempre con []
    #field.name: ese field es el nombre inventado. puedo poner campo.name
    #Se hace un array para que coja todos los campos en vez de ponerlos manualmente.
    #meta.get_fields: leer todos los campos que encuentra.
    #if hasattr (has attribute)
    #verbose_name: label o etiqueta, si no lo pongo va a explotar si encuentra las etiquetas verbose_name bien puestas.
    search_fields = ('id','empresa')
    list_filter   = ('id','empresa')
admin.site.register(Entrevistador, EntrevistadorAdmin)#el modelo se llama Entrevistador y ha sido registrado por entreAdmin

class CurriculumAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Curriculum._meta.get_fields() if hasattr(field, 'verbose_name')] #es una lista, siempre con []
    #field.name: ese field es el nombre inventado. puedo poner campo.name
    #Se hace un array para que coja todos los campos en vez de ponerlos manualmente.
    #meta.get_fields: leer todos los campos que encuentra.
    #if hasattr (has attribute)
    #verbose_name: label o etiqueta, si no lo pongo va a explotar si encuentra las etiquetas verbose_name bien puestas.
    search_fields = ('id','nombre')
    list_filter   = ('id','nombre')
admin.site.register(Curriculum, CurriculumAdmin)#el modelo se llama Entrevistador y ha sido registrado por entreAdmin


admin.site.register(DetalleCurriculumEstudio)
admin.site.register(DetalleCurriculumExperiencia)

class NoticiaAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Noticia._meta.get_fields() if hasattr(field,'verbose_name')]
    search_fields = ('id','titulo')
admin.site.register(Noticia, NoticiaAdmin)






























