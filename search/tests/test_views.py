"""File containing django view tests for ride search functionality"""
from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch

class TestViews(TestCase):
    """Test class to test Django views for ride creation functionality"""
    def setUp(self):
        self.client = Client()
        self.search_url = reverse("search")
        self.request_ride_url = reverse("request_ride", args=["078508ce-2efc-4316-8987-12b9551be5b4"])
        self.mock_users_collection = patch("search.views.users_collection").start()
        self.mock_rides_collection = patch("search.views.rides_collection").start()
        self.mock_initialize_database = patch("search.views.initialize_database").start()
        self.mock_get_recommended_ride = patch("search.views.get_recommended_ride").start()
        self.addCleanup(patch.stopall)

    def test_search_logged_out_user(self):
        """Tests for searching logged out user"""
        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/index/")



    def test_search_logged_in_user(self):
        """Tests for searching logged in user"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        self.mock_users_collection.find_one.return_value = {
            "username": "test",
            "travel_preferences": "Comfort",
            "likes": ["music", "quiet"],
            "is_smoker": True,
            "travel_with_pets": False,
            "driver_gender": "Any",
        }
        self.mock_rides_collection.find.return_value = [
            {"_id": "ride1", "owner": "another_user", "destination": "City A"},
            {"_id": "ride2", "owner": "another_user", "destination": "City B"},
        ]
        self.mock_get_recommended_ride.return_value = {
            "id": "ride1",
            "owner": "another_user",
            "destination": "City A",
        }

        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)  # pylint: disable=deprecated-method
        self.assertTemplateUsed(response, "search/search.html")
#    def test_search_logged_in_user(self):
#        """Tests for searching logged in user"""
#        session = self.client.session
#        session["username"] = "test"
#        session.save()
#        response = self.client.get(self.search_url)
#        # go to requests page
#        self.assertEqual(response.status_code, 200) # pylint: disable=deprecated-method
#        self.assertTemplateUsed(response, "search/search.html")

    def test_request_ride(self):
        """Tests for requesting ride"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.request_ride_url)
        # go to requests page
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_search_index_no_user_data(self):
        """Test search_index when user has no preferences in the database."""
        session = self.client.session
        session["username"] = "testuser"
        session.save()
        self.mock_users_collection.find_one.return_value = None
        self.mock_rides_collection.find.return_value = [
            {"_id": "ride1", "owner": "another_user", "destination": "City A"},
            {"_id": "ride2", "owner": "another_user", "destination": "City B"},
        ]

        response = self.client.get(self.search_url)
        self.assertEqual(response.status_code, 200)  # pylint: disable=deprecated-method
        self.assertTemplateUsed(response, "search/search.html")
        self.assertIn("rides", response.context)
        self.assertIn("recommended_ride", response.context)
        self.assertEqual(response.context["recommended_ride"]["id"], "ride1")
