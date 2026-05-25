from django.test import SimpleTestCase
from django.urls import reverse


class HomePageTests(SimpleTestCase):
    def test_home_page_renders_uploaded_html(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Hi, I&#x27;m mdull')
        self.assertContains(response, '/static/css/fontawesome7.min.css')
        self.assertContains(response, '/static/images/photo_2026-05-17_19-13-54.jpg')

    def test_admin_is_available(self):
        response = self.client.get('/admin/')

        self.assertEqual(response.status_code, 302)
        self.assertIn('/admin/login/', response['Location'])
