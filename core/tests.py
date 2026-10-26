from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Servicio


class ServicioListTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_model = get_user_model()
        cls.user = user_model.objects.create_user(
            username='propietario',
            password='test-password-123',
        )
        cls.other_user = user_model.objects.create_user(
            username='otro',
            password='test-password-123',
        )

        Servicio.objects.create(
            propietario=cls.user,
            titulo='Diseño web',
            descripcion='Sitio web profesional',
            precio='150.00',
            categoria='Diseño',
        )
        Servicio.objects.create(
            propietario=cls.user,
            titulo='Asesoría fiscal',
            descripcion='Consulta de impuestos',
            precio='80.00',
            categoria='Finanzas',
        )
        Servicio.objects.create(
            propietario=cls.other_user,
            titulo='Servicio privado',
            descripcion='No debe aparecer',
            precio='99.00',
            categoria='Privado',
        )

    def setUp(self):
        self.client.force_login(self.user)

    def test_list_only_shows_services_owned_by_current_user(self):
        response = self.client.get(reverse('servicios'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Diseño web')
        self.assertContains(response, 'Asesoría fiscal')
        self.assertNotContains(response, 'Servicio privado')

    def test_search_matches_title_description_and_category(self):
        for query, expected in (
            ('Diseño', 'Diseño web'),
            ('impuestos', 'Asesoría fiscal'),
            ('Finanzas', 'Asesoría fiscal'),
        ):
            with self.subTest(query=query):
                response = self.client.get(reverse('servicios'), {'q': query})

                self.assertEqual(response.status_code, 200)
                self.assertContains(response, expected)
                self.assertNotContains(response, 'Servicio privado')

    def test_search_and_pagination_retain_current_user_scope(self):
        for number in range(11):
            Servicio.objects.create(
                propietario=self.user,
                titulo=f'Diseño adicional {number}',
                descripcion='Servicio de prueba',
                precio='25.00',
                categoria='Diseño',
            )

        response = self.client.get(reverse('servicios'), {'q': 'Diseño', 'page': 2})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page_obj'].number, 2)
        self.assertContains(response, 'Página 2 de 2')
        self.assertNotContains(response, 'Servicio privado')

    def test_invalid_page_numbers_fall_back_to_a_valid_page(self):
        invalid_response = self.client.get(
            reverse('servicios'),
            {'page': 'not-a-page'},
        )
        out_of_range_response = self.client.get(
            reverse('servicios'),
            {'page': '99'},
        )

        self.assertEqual(invalid_response.status_code, 200)
        self.assertEqual(invalid_response.context['page_obj'].number, 1)
        self.assertEqual(out_of_range_response.status_code, 200)
        self.assertEqual(out_of_range_response.context['page_obj'].number, 1)

    def test_list_requires_login(self):
        self.client.logout()

        response = self.client.get(reverse('servicios'))

        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('servicios')}",
        )


class ServicioOwnershipTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.owner = user_model.objects.create_user(
            username='owner',
            password='test-password-123',
        )
        self.other_user = user_model.objects.create_user(
            username='intruso',
            password='test-password-123',
        )
        self.servicio = Servicio.objects.create(
            propietario=self.owner,
            titulo='Servicio privado',
            descripcion='Solo para su propietario',
            precio='50.00',
            categoria='Prueba',
        )

    def test_other_user_cannot_edit_or_delete_service(self):
        self.client.force_login(self.other_user)

        edit_response = self.client.get(
            reverse('editar_servicio', args=[self.servicio.pk])
        )
        delete_response = self.client.get(
            reverse('eliminar_servicio', args=[self.servicio.pk])
        )

        self.assertEqual(edit_response.status_code, 404)
        self.assertEqual(delete_response.status_code, 404)
        self.assertTrue(Servicio.objects.filter(pk=self.servicio.pk).exists())

    def test_owner_can_create_edit_and_delete_service(self):
        self.client.force_login(self.owner)

        create_response = self.client.post(
            reverse('crear_servicio'),
            {
                'titulo': 'Nuevo servicio',
                'descripcion': 'Descripción de prueba',
                'precio': '75.00',
                'categoria': 'Prueba',
            },
        )
        self.assertRedirects(create_response, reverse('servicios'))

        created_service = Servicio.objects.get(titulo='Nuevo servicio')
        self.assertEqual(created_service.propietario, self.owner)

        edit_response = self.client.post(
            reverse('editar_servicio', args=[self.servicio.pk]),
            {
                'titulo': 'Servicio actualizado',
                'descripcion': 'Descripción actualizada',
                'precio': '60.00',
                'categoria': 'Actualizada',
            },
        )
        self.assertRedirects(edit_response, reverse('servicios'))
        self.servicio.refresh_from_db()
        self.assertEqual(self.servicio.titulo, 'Servicio actualizado')

        delete_response = self.client.post(
            reverse('eliminar_servicio', args=[self.servicio.pk])
        )
        self.assertRedirects(delete_response, reverse('servicios'))
        self.assertFalse(Servicio.objects.filter(pk=self.servicio.pk).exists())
