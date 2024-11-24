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
        self.feedback_url = reverse("feedback", args=[1])  # Assuming ride_id is passed as 1
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


    @patch("user.views.initialize_database")
    @patch("user.views.feedback_collection.insert_one")
    @patch("user.views.rides_collection.update_one")
    def test_feedback_post_valid(self, mock_update, mock_insert, mock_init_db):
        # Setup session and valid feedback data
        self.client.session['username'] = 'testuser'  # Set the session username
        self.client.session.save()

        feedback_data = {
            'ride_rating': 5,  # Example rating
            'driver_rating': 5,  # Provide a value for driver_rating
            'feedback': 'Great ride!',  # Provide a value for feedback
        }

        # Mock database methods if needed (to prevent actual database calls)
        mock_init_db.return_value = None  # Mock the DB initialization
        mock_insert.return_value = None  # Mock insert_one to prevent actual DB insertion
        mock_update.return_value = None  # Mock update_one

        # Send a POST request to the feedback URL with valid data
        response = self.client.post(self.feedback_url, data=feedback_data)

        # Assert that the insert_one method was called once (indicating feedback was saved)
        mock_insert.assert_called_once()

        # Optionally, check if the response redirects to the correct page (e.g., the index page)
        self.assertRedirects(response, reverse("index"))

    @patch("user.views.feedback_collection.insert_one")
    @patch("user.views.rides_collection.update_one")
    def test_feedback_post_invalid(self, mock_update, mock_insert):
        """Test submitting invalid feedback (POST request)"""
        # Simulate invalid POST data (missing required fields)
        feedback_data = {
            "ride_rating": 5,  # Missing driver_rating and feedback fields
        }

        # Simulate a POST request to the feedback view with invalid data
        response = self.client.post(self.feedback_url, data=feedback_data)

        # Check if the form was re-rendered due to invalid data
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/feedback.html")

        # Ensure the insert_one and update_one methods were NOT called
        mock_insert.assert_not_called()
        mock_update.assert_not_called()

    def test_feedback_get(self):
        """Test the GET request for the feedback form"""
        response = self.client.get(self.feedback_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "user/feedback.html")