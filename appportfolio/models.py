# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from turtledemo.sorting_animate import Block

from django.db import models
from django.contrib.auth.models import User


################################################
# TABLA 1 - Habilidades 
################################################

class Habilidad(
    models.Model):  # MODELS.MODEL es como el extend, solo que aquí no se pone extende, es como el extend thread, para saber que es un modelo
    id = models.AutoField(primary_key=True)  # le indico la pk
    habilidad = models.CharField("Nombre de Habilidad", max_length=25, null=True,
                                 blank=True)  # CharField = varchar, "Nombre " es la label/etiqueta, null true es que puede ser nulo, ni coma ni ;. nulo es nada y blanco es espacio
    nivel = models.IntegerField("Nivel", null=True, blank=True)  # un ejemplo de una columna (nivel del 1-10)
    descripcion = models.TextField("Descripcion", null=True, blank=True)

    class Meta:  # Dentro de la clase hay otra clase, clases anidadas. su efecto es configurar a la otra clase "Habilidad"
        verbose_name = "Habilidad"  # verbouse: nombre detallado, es el nombre de la tabla
        verbose_name_plural = "Habilidades"  # nombre externo de la tabla, el nombre de verdad, si no lo pongo el nombre le añade una s: camions
        ordering = ['habilidad']  # ordenar por el campo habilidad

    def __str__(
            self):  # esto es un méto do porque pertenece a una clase. #__str__ todo lo que lleve los guiones es python de la comunidad, y es un toString()
        return '%s,%s, %s' % (self.habilidad, self.nivel,
                              self.descripcion)  # self es el this de java. % este es el que separa el formato y los campos.
        # este méto do funciona como tostring

################################################
# TABLA 2 - Personal
################################################
class Personal(models.Model): #extiende de Model
    id = models.AutoField(primary_key=True)
    nombre = models.CharField("Nombre", max_length=25, null=True, blank=True)
    apellido1 = models.CharField("Primer Apellido", max_length=25, null=True, blank=True)
    apellido2 = models.CharField("Segundo Apellido", max_length=25, null=True, blank=True)
    edad = models.IntegerField("Edad", null=True, blank=True)
    usuario=models.ForeignKey(User,related_name='datos_usuario',null=True, blank=True,on_delete=models.PROTECT)
    #related_name: nombre de la relacion, un alias
    #on_delete=models.PROTECT(): proteger el borrado en cascada (ej. si borro usuarios que no se borren las facturas (por estan relacionadas))
    class Meta:
        verbose_name = "Personal"
        verbose_name_plural = "Personales"
        ordering = ['nombre']

    def __str__(self):
        return '%s,%s,%s,%s,%s' % (self.id, self.nombre, self.apellido1, self.apellido2, self.edad)

################################################
# TABLA 3 - Categorias
################################################
class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_categoria = models.CharField("Puesto de Trabajo", max_length=30, null=True, blank=True)

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['nombre_categoria']

    def __str__(self):
        return '%s,%s' % (self.id, self.nombre_categoria)

################################################
# TABLA 4 - Estudios
################################################
class Estudio(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField("Titulo", max_length=30, null=True, blank=True)
    fechaInicio = models.DateField("Fecha Inicio", null=True, blank=True)
    fechaFin = models.DateField("Fecha Fin", null=True, blank=True)
    notamedia = models.IntegerField("Nota Media", null=True, blank=True)
    lugarEstudio = models.CharField("Lugar de Estudio", max_length=30, null=True, blank=True)
    nombreLugar = models.CharField("Nombre de Lugar", max_length=30, null=True, blank=True)
    ciudad = models.CharField("Ciudad", max_length=30, null=True, blank=True)
    presencial = models.BooleanField("Presencial", null=True, blank=True)
    observaciones = models.TextField("Observaciones", null=True, blank=True)

    class Meta:
        verbose_name = "Estudio"
        verbose_name_plural = "Estudios"
        ordering = ['fechaInicio']

    def __str__(self):
        return '%s, %s, %s, %s, %s, %s, %s, %s, %s' % (
            self.id, self.titulo, self.fechaInicio, self.fechaFin, self.notamedia, self.nombreLugar,
            self.ciudad, self.presencial, self.observaciones
        )


################################################
# 5 - Experiencias
################################################
class Experiencia(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.CharField('Empresa', max_length=50, null=True, blank=True)
    fecha_inicio = models.DateField('Fecha de Inicio', null=True, blank=True)
    fecha_fin = models.DateField('Fecha de Finalización', null=True, blank=True)
    observaciones = models.CharField('Observaciones', max_length=50, null=True, blank=True)
    categoria = models.CharField('Categorias', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = 'Experiencia'  # puede ser otro nombre
        verbose_name_plural = 'Experiencias'
        ordering = ['empresa']

    def __str__(self):
        return '%s,%s' % (self.id,self.empresa)

################################################
# 6 - Imagen
################################################
class Imagen(models.Model):
    id = models.AutoField(primary_key=True)
    imagen = models.ImageField('Imagen', max_length=50, null=True, blank=True, upload_to='imágenes/')
    comentario= models.CharField("Comentario", max_length=100, null=True, blank=True)
    #fk_estudio=models.ForeignKey(Estudio,related_name='imagenes_estudio',on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Imagen'
        verbose_name_plural = 'Imagenes'
        ordering = ['id']
    def __str__(self):
        return '%s,%s' % (self.id,self.imagen)
################################################
# 7 - Video
################################################
class Video(models.Model):
    id = models.AutoField(primary_key=True)
    video=models.FileField("Video", blank=True, null=True,upload_to='videos/')
    comentario = models.CharField("Comentario", max_length=100, null=True, blank=True)
    class Meta:
        verbose_name = 'Video'
        verbose_name_plural = 'Videos'
        ordering = ['id']
    def __str__(self):
        return '%s,%s,%s' % (self.id,self.video,self.comentario)

################################################
# 8 - Entrevistador
################################################
class Entrevistador(models.Model):
    id = models.AutoField(primary_key=True)
    avatar=models.ImageField('Avatar', null=True, blank=True, upload_to='media/')
    empresa=models.CharField('Empresa', max_length=30, null=True, blank=True)
    fecha_entrevista=models.DateField('Fecha de Entrevista', null=True, blank=True)
    conectado=models.BooleanField('Conectado', null=True, blank=True)
    seleccionado=models.BooleanField('Seleccionado', null=True, blank=True)
    notas=models.TextField("Notas", null=True, blank=True)
    #foreign keys
    user=models.ForeignKey(User,related_name='entrevistas_usuario',null=True, blank=True,on_delete=models.PROTECT)
    class Meta:
        verbose_name = 'Entrevistador'
        verbose_name_plural = 'Entrevistadores'
        ordering = ['empresa']
    def __str__(self):
        return "%s,%s" % (self.empresa, self.user)

################################################
# 9 - Curriculum
################################################
class Curriculum(models.Model):
    id = models.AutoField(primary_key=True)
    nombre=models.CharField('Nombre', max_length=30, null=True, blank=True)
    ap1=models.CharField('Ap1', max_length=30, null=True, blank=True)
    ap2 = models.CharField('Ap2', max_length=30, null=True, blank=True)
    email=models.EmailField('Email', null=True, blank=True)
    telefono=models.CharField('Teléfono', max_length=30, null=True, blank=True)
    class Meta:
        verbose_name = 'Curriculum'
        verbose_name_plural = 'Curriculums'
        ordering = ['id']
    def __str__(self):
        return '%s,%s' % (self.id, self.nombre)

################################################
# 10 - DetalleCurriculoEstudios
################################################
class DetalleCurriculumEstudio(models.Model):
    id = models.AutoField(primary_key=True)
    fk_Detalle_Estudio = models.ForeignKey(Estudio, related_name='detalle_estudios', null=True, blank=True, on_delete=models.PROTECT)
    fk_Curriculum = models.ForeignKey(Curriculum, related_name='curriculum_estudios', null=True, blank=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'DetalleEstudio'
        verbose_name_plural = 'DetalleEstudios'
        ordering = ['id']

    def __str__(self):
        titulo = self.fk_Detalle_Estudio.titulo if self.fk_Detalle_Estudio else 'No asignado'
        return '%s,%s' % (self.id, titulo)


# Solo un marcador de posición


#################################################
# 11 - DetalleCurriculoExperiencias
################################################
class DetalleCurriculumExperiencia(models.Model):
    id = models.AutoField(primary_key=True)
    fk_Detalle_Experiencia = models.ForeignKey(Experiencia, related_name='detalle_experiencias', null=True, blank=True, on_delete=models.PROTECT)
    fk_Curriculum = models.ForeignKey(Curriculum, related_name='curriculum_experiencias', null=True, blank=True,on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'DetalleExperiencia'
        verbose_name_plural = 'DetalleExperiencias'
        ordering = ['id']
    def __str__(self):
        return '%s' % (self.id)




class Noticia(models.Model):
    id = models.AutoField(primary_key=True)
    titulo=models.CharField('Titulo', max_length=200, null=True, blank=True)
    contenido=models.TextField('Contenido', null=True, blank=True)
    fecha_creacion=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    imagen=models.ImageField('Imagen',  null=True, blank=True, upload_to='media/')

    def __str__(self):
        return '%s,%s' % (self.id, self.titulo)




































