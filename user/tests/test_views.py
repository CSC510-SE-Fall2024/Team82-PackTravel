from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from unittest.mock import patch


"""Test cases for user views, including registration, login, logout, and index page functionality."""

class TestViews(TestCase):
    """Test case class for testing views like index, register, login, and logout."""
    def setUp(self):
        self.client = Client()
        self.index_url = reverse("index")
        self.register_url = reverse("register")
        self.logout_url = reverse("logout")
        self.login_url = reverse("login")
        self.ride_history_url = reverse("ride_history")
        self.test_user = User.objects.create_user(username="testuser", password="12345")
        self.mock_rides = [
            {"ride_id": "1", "confirmed_users": ["testuser"], "destination": "Destination A"},
            {"ride_id": "2", "confirmed_users": ["testuser"], "destination": "Destination B"},
        ]

    def test_index(self):
        """Test the index page loads successfully and uses the correct template."""
        response = self.client.get(self.index_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/home.html")

    def test_register(self):
        """Test the register page loads successfully and uses the correct template."""
        response = self.client.get(self.register_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/register.html")

    def test_login(self):
        """Test the login page loads successfully and uses the correct template."""
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_logout(self):
        """Test the logout page loads successfully and uses the correct template."""
        self.client.login(username="testuser", password="12345")
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_login_invalid_credentials(self):
        """Test the login page loads successfully and uses the correct template."""
        response = self.client.post(self.login_url, 
        {"username": "wronguser", "password": "wrongpass"})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")
     
    def test_register_post_valid_data(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password1": "complex_password123",
            "password2": "complex_password123"
        })
        self.assertEqual(response.status_code, 200)

    def test_register_post_invalid_data(self):
        response = self.client.post(self.register_url, {
            "username": "newuser",
            "password1": "password",
            "password2": "different_password"
        })
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_login_post_invalid_username(self):
        response = self.client.post(self.login_url, {
            "username": "nonexistentuser",
            "password": "12345"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_login_post_invalid_password(self):
        response = self.client.post(self.login_url, {
            "username": "testuser",
            "password": "wrongpassword"
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/login.html")

    def test_logout_unauthenticated_user(self):
        response = self.client.get(self.logout_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("index"))

    def test_csrf_token_present(self):
        response = self.client.get(self.login_url)
        self.assertContains(response, 'csrfmiddlewaretoken')


    @patch("user.views.initialize_database")  # Replace "yourapp" with your actual app name
    @patch("user.views.rides_collection.find")
    def test_ride_history_logged_in(self, mock_find, mock_initialize_db):
        """Test the ride history page for a logged-in user with completed rides."""
        mock_find.return_value = self.mock_rides

        session = self.client.session
        session["username"] = "testuser"
        session.save()

        response = self.client.get(self.ride_history_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/ride_history.html")
        self.assertContains(response, "Destination A")
        self.assertContains(response, "Destination B")

    def test_ride_history_not_logged_in(self):
        """Test the ride history page redirects for a user not logged in."""
        response = self.client.get(self.ride_history_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.index_url)
        session = self.client.session
        self.assertEqual(session.get("alert"), "Please login to view your ride history")