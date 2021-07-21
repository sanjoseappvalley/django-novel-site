from django.test import TestCase

# Create your tests here.
class RegisterViewTest(TestCase):

    def test_redirect_to_home_page(self):
        name = 'aaaa'
        email = 'aaaa@gmail.com'
        password1 = 'aaaa1234'
        password2 = 'aaaa1234'
        response = self.client.post('/register/', data={'username': name, 'email': email, 'password1': password1, 'password2': password2})
        self.assertRedirects(response, '/login/')

    def test_success_register_message(self):
        name = 'aaaa'
        email = 'aaaa@gmail.com'
        password1 = 'aaaa1234'
        password2 = 'aaaa1234'
        response = self.client.post('/register/', data={'username': name, 'email': email, 'password1': password1, 'password2': password2}, follow=True)
        message = list(response.context['messages'])[0]
        self.assertEqual(
            message.message,
            "Account created for aaaa!"
        )
        self.assertEqual(message.tags, "success")
