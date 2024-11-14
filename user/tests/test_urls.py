"""Django url tests for user login and sign up functionality"""
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from user.views import index, register, logout, login

class TestUrl(SimpleTestCase):
    """Django class to test urls for user login and sign up functionality"""

    def test_index_resolved(self):
        """Tests for Index URL resolution"""
        url = reverse('index')
        self.assertEqual(resolve(url).func, index) # pylint: disable=deprecated-method

    def test_register_resolved(self):
        """Tests for Register URL resolution"""
        url = reverse('register')
        self.assertEqual(resolve(url).func, register) # pylint: disable=deprecated-method

    def test_login_resolved(self):
        """Tests for Login URL resolution"""
        url = reverse('login')
        self.assertEqual(resolve(url).func, login) # pylint: disable=deprecated-method

    def test_logout_resolved(self):
        """Tests for Logout URL resolution"""
        url = reverse('logout')
        self.assertEqual(resolve(url).func, logout) # pylint: disable=deprecated-method
