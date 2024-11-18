# tests.py
import os  # Usado para interactuar con el sistema de archivos, como la eliminación de archivos.
from django.test import TestCase  # Clase de Django que facilita la creación de pruebas unitarias.
from django.test import override_settings  # Permite sobrescribir configuraciones en un entorno de prueba, como MEDIA_ROOT.
from appportfolio.models import Noticia  # Importación del modelo Noticia.
from django.core.files.uploadedfile import SimpleUploadedFile  # Facilita la creación de archivos simulados.
from os.path import basename  # Extrae el nombre base del archivo (sin la ruta).
import tempfile  # Usado para crear directorios temporales donde almacenar los archivos durante las pruebas.
from uuid import uuid4  # Para generar un nombre único para la imagen.

# Decorador que cambia la ruta MEDIA para pruebas
@override_settings(MEDIA_ROOT=tempfile.mkdtemp())
class NoticiaModelTest(TestCase):
    #Nombre de clase a testear + ModelTest, modelo de prueba.

    # def tearDown(self):#méto-do para borrar
    #     #El def aquí es un méto-do xq va dentro de una clase.
    #     # Méto-do especial de Django para eliminar archivos después de las pruebas.
    #     for noticia in Noticia.objects.all():
    #         if noticia.imagen and noticia.imagen.path:#si existe la imagen y el camino:
    #             os.remove(noticia.imagen.path)#quita el pathc
    #     super().tearDown()#recolector basura

    #caja blanca.
    def test_creacion_noticia_sin_imagen(self):
        # Prueba que una noticia se puede crear sin proporcionar una imagen.
        noticia = Noticia.objects.create(#es lo mismo que noticia=Noticia(), constructor.ya abajo sería noticia.titulo="", noticia.save(). el usado ahora es más rapido
            #creamos un prueba (up)
            titulo="Noticia sin imagen",
            contenido="Contenido de prueba sin imagen"
        )
        self.assertEqual(noticia.titulo, "Noticia sin imagen")#comprobación de base de datos. para ver si se ha insertado bien.
        self.assertEqual(noticia.contenido, "Contenido de prueba sin imagen")#contrario: assertNotEqual.
        self.assertFalse(noticia.imagen)  # Verificar que no se asignó imagen.

    def test_creacion_noticia_con_imagen(self):
        # Prueba que una noticia se puede crear con una imagen cargada.
        #unique_filename = f'test_image_{uuid4().hex}.jpg'#concatena para q no choquen los nombre.
        unique_filename="prueba.jpg"
        image_data = SimpleUploadedFile(
            name=unique_filename,
            content=b'algun contenido de la imagen',#b : convierte a binario lo qye viene a la derecha.equivale al contenido de imagen.para que no esté vacia.
            content_type='image/jpeg'
        )
        noticia = Noticia.objects.create(
            titulo="Noticia con imagen",
            contenido="Contenido con imagen",
            imagen=image_data
        )
        self.assertEqual(noticia.titulo, "Noticia con imagen")
        self.assertEqual(noticia.contenido, "Contenido con imagen")
        self.assertIsNotNone(noticia.imagen)  # La imagen no debería estar vacía.
        self.assertEqual(basename(noticia.imagen.name), unique_filename)  # Comparar con el nombre dinámico generado.
