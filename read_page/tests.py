from django.test import TestCase, Client

# Create your tests here.

class MainTest(TestCase):
    def test_main_url_is_exist(self):
        response = Client().get('/read_page/')
        self.assertEqual(response.status_code, 200)

    def test_main_using_main_template(self):
        response = Client().get('/read_page/')
        self.assertTemplateUsed(response, 'read_page.html')