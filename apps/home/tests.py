from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Estudiante
from .forms import EstudianteForm

class EstudianteModelTests(TestCase):

    def setUp(self):
        self.estudiante = Estudiante.objects.create(
            nombre='Juan',
            apellido='Pérez',
            cedula='12345678',
            telefono='04141234567',
            email='juan.perez@example.com',
            ano_ingreso=2020,
            carrera='Ingeniería',
            estado_solicitud='Pendiente',
            es_egresado=False
        )

    def test_crear_estudiante(self):
        self.assertEqual(self.estudiante.nombre, 'Juan')

    def test_actualizar_estudiante(self):
        self.estudiante.nombre = 'Carlos'
        self.estudiante.save()
        self.assertEqual(self.estudiante.nombre, 'Carlos')

    def test_eliminar_estudiante(self):
        self.estudiante.delete()
        self.assertEqual(Estudiante.objects.count(), 0)


class EstudianteFormTests(TestCase):

    def test_form_valido(self):
        form_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'cedula': '12345678',
            'telefono': '04141234567',
            'email': 'juan.perez@example.com',
            'ano_ingreso': 2020,
            'carrera': 'Ingeniería',
            'estado_solicitud': 'Pendiente',
            'es_egresado': False
        }
        form = EstudianteForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_telefono_invalido(self):
        form_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'cedula': '12345678',
            'telefono': '0414ABCD123',  # Teléfono inválido
            'email': 'juan.perez@example.com',
            'ano_ingreso': 2020,
            'carrera': 'Ingeniería',
            'estado_solicitud': 'Pendiente',
            'es_egresado': False
        }
        form = EstudianteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['telefono'], ['El teléfono debe tener 10 dígitos.'])

    def test_form_email_invalido(self):
        form_data = {
            'nombre': 'Juan',
            'apellido': 'Pérez',
            'cedula': '12345678',
            'telefono': '04141234567',
            'email': 'juan.perez@',  # Email inválido
            'ano_ingreso': 2020,
            'carrera': 'Ingeniería',
            'estado_solicitud': 'Pendiente',
            'es_egresado': False
        }
        form = EstudianteForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'], ['El correo electrónico no es válido.'])


class EstudianteViewTests(TestCase):

    def setUp(self):
        self.estudiante1 = Estudiante.objects.create(
            nombre='Juan',
            apellido='Pérez',
            cedula='12345678',
            telefono='04141234567',
            email='juan.perez@example.com',
            ano_ingreso=2020,
            carrera='Ingeniería',
            estado_solicitud='Pendiente',
            es_egresado=False
        )
        self.estudiante2 = Estudiante.objects.create(
            nombre='Carlos',
            apellido='Martínez',
            cedula='87654321',
            telefono='04141234568',
            email='carlos.martinez@example.com',
            ano_ingreso=2021,
            carrera='Derecho',
            estado_solicitud='Aprobado',
            es_egresado=False
        )
        self.user = get_user_model().objects.create_user(username='testuser', password='12345')

    def test_lista_estudiantes(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('lista_estudiantes', args=[0]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan')

    def test_crear_estudiante_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('crear_estudiante'), {
            'nombre': 'Carlos',
            'apellido': 'Martínez',
            'cedula': '87654321',
            'telefono': '04141234568',
            'email': 'carlos.martinez@example.com',
            'ano_ingreso': 2021,
            'carrera': 'Derecho',
            'estado_solicitud': 'Pendiente',
            'es_egresado': False
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras creación

    def test_actualizar_estudiante_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('actualizar_estudiante', args=[self.estudiante1.pk]), {
            'nombre': 'Carlos',
            'apellido': 'Martínez',
            'cedula': '12345678',
            'telefono': '04141234567',
            'email': 'carlos.martinez@example.com',
            'ano_ingreso': 2020,
            'carrera': 'Ingeniería',
            'estado_solicitud': 'Aprobado',
            'es_egresado': False
        })
        self.assertEqual(response.status_code, 302)  # Redirección tras actualización
        self.estudiante1.refresh_from_db()
        self.assertEqual(self.estudiante1.nombre, 'Carlos')
        self.assertEqual(self.estudiante1.estado_solicitud, 'Aprobado')

    def test_eliminar_estudiante_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('eliminar_estudiante', args=[self.estudiante1.pk]))
        self.assertEqual(response.status_code, 302)  # Redirección tras eliminación
        self.assertEqual(Estudiante.objects.count(), 1)

    def test_busqueda_estudiantes_nombre(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('lista_estudiantes', args=[0]), {'q': 'Juan'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan')
        self.assertNotContains(response, 'Carlos')

    def test_busqueda_estudiantes_apellido(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('lista_estudiantes', args=[0]), {'q': 'Martínez'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carlos')
        self.assertNotContains(response, 'Juan')

    def test_busqueda_estudiantes_cedula(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('lista_estudiantes', args=[0]), {'q': '12345678'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Juan')
        self.assertNotContains(response, 'Carlos')

    def test_busqueda_y_paginacion(self):
        self.client.login(username='testuser', password='12345')
        # Crear más estudiantes para probar la paginación
        for i in range(1, 21):
            Estudiante.objects.create(
                nombre=f'Estudiante{i}',
                apellido='Apellido',
                cedula=f'Cedula{i}',
                telefono='04141234567',
                email=f'estudiante{i}@example.com',
                ano_ingreso=2020,
                carrera='Ingeniería',
                estado_solicitud='Pendiente',
                es_egresado=False
            )
        response = self.client.get(reverse('lista_estudiantes', args=[0]), {'q': 'Estudiante', 'page': 2})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Estudiante11')
        self.assertContains(response, 'Estudiante20')
        self.assertNotContains(response, 'Estudiante1')
