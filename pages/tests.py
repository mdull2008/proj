from django.contrib import admin
from django.test import TestCase
from django.urls import reverse
from django.contrib.staticfiles import finders

from .models import Skill


class HomePageTests(TestCase):
    def test_home_page_renders_uploaded_html(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hi, I'm mdull")
        self.assertContains(response, '/static/css/fontawesome7.min.css')
        self.assertContains(response, '/static/images/photo_2026-05-17_19-13-54.jpg')
        self.assertContains(response, 'href="#models-database-skill"')
        self.assertContains(response, 'Models and Databases')

    def test_uploaded_static_assets_are_discoverable(self):
        self.assertIsNotNone(finders.find('css/fontawesome7.min.css'))
        self.assertIsNotNone(finders.find('fonts/fa-solid-900.woff2'))
        self.assertIsNotNone(finders.find('images/photo_2026-05-17_19-13-54.jpg'))

    def test_admin_is_available(self):
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])

    def test_skill_model_is_registered_in_admin(self):
        self.assertIn(Skill, admin.site._registry)
