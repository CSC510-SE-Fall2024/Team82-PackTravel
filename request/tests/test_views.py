"""File containing django view tests for ride management functionality"""
from django.test import TestCase, Client
from django.urls import reverse
from pymongo import MongoClient
from django.core.mail import send_mail
from request.views import send_capacity_mail
from unittest.mock import patch
from django.conf import settings

class TestViews(TestCase):
    """Test class to test Django views for ride creation functionality"""
    def setUp(self):
        self.client = Client()
        self.requested_rides_url = reverse("requests")
        self.cancel_ride_url = reverse("cancel_ride", args=["078508ce-2efc-4316-8987-12b9551be5b4"])
        self.cancel_accepted_requests_url = reverse("cancel_accepted_request", args=["078508ce-2efc-4316-8987-12b9551be5b4", "test"])
        self.accept_request_url = reverse("accept_request", args=["078508ce-2efc-4316-8987-12b9551be5b4", "test"])
        self.reject_request_url = reverse("reject_request", args=["078508ce-2efc-4316-8987-12b9551be5b4", "test"])
        self.delete_ride_url = reverse("delete_ride", args=["078508ce-2efc-4316-8987-12b9551be5b4"])
    
    # Initialize database connection
        self.client_db = MongoClient("mongodb+srv://sohampatil195:pJ9WIORj17gaznOZ@testcluster.zwau0.mongodb.net/?retryWrites=true&w=majority&appName=TestCluster")
        self.db_handle = self.client_db.test_db
        self.rides_collection = self.db_handle.rides
        self.users_collection = self.db_handle.users

        # Insert a test ride
        self.rides_collection.insert_one({
            "_id": "078508ce-2efc-4316-8987-12b9551be5b4",
            "owner": "test_owner",
            "destination": "destination",
            "availability": 1,
            "requested_users": ["test"],
            "confirmed_users": []
        })

        # Insert a test user
        self.users_collection.insert_one({
            "username": "test_owner",
            "email": "test_owner@example.com"
        })
    
    def tearDown(self):
        # Clean up the test database
        self.rides_collection.delete_many({})
        self.users_collection.delete_many({})

    def test_requested_rides(self):
        """Tests for ride requested"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.requested_rides_url)
        self.assertEqual(response.status_code, 200) # pylint: disable=deprecated-method
        self.assertTemplateUsed(response, "requests/requests.html")

    def test_cancel_ride_logged_in_user(self):
        """Tests for ride canceled for logged in user"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.cancel_ride_url)
        # go to requests page
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_accept_ride_request(self):
        """Tests for ride accepted"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.accept_request_url)
        # go to requests page
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

        notifications = Notification.objects.filter(username="test")
        self.assertEqual(notifications.count(), 1)
        self.assertEqual(notifications.first().message, 'Your request to join the ride to destination has been accepted.')

    def test_reject_ride_request(self):
        """Tests for ride rejected"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.reject_request_url)
        # go to requests page
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_cancel_accepted_ride(self):
        """Tests for accepted ride cancellation"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.cancel_accepted_requests_url)
        # go to requests page
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_delete_ride_not_logged_in(self):
        """Tests for delete ride when user is not logged in"""
        response = self.client.get(self.delete_ride_url)
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/index/")
        session = self.client.session
        self.assertEqual(session["alert"], "Please login to cancel rides.")

    def test_delete_ride_not_found(self):
        """Tests for delete ride when ride is not found"""
        session = self.client.session
        session["username"] = "test_owner"
        session.save()
        response = self.client.get(reverse("delete_ride", args=["non_existent_ride_id"]))
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_delete_ride_not_owner(self):
        """Tests for delete ride when user is not the owner"""
        session = self.client.session
        session["username"] = "test"
        session.save()
        response = self.client.get(self.delete_ride_url)
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")

    def test_delete_ride_owner(self):
        """Tests for delete ride when user is the owner"""
        session = self.client.session
        session["username"] = "test_owner"
        session.save()
        response = self.client.get(self.delete_ride_url)
        self.assertEqual(response.status_code, 302) # pylint: disable=deprecated-method
        self.assertRedirects(response, "/requests/")
        ride = self.rides_collection.find_one({"_id": "078508ce-2efc-4316-8987-12b9551be5b4"})
        self.assertIsNone(ride)
    
    @patch('request.views.send_mail')
    def test_send_capacity_mail_success(self, mock_send_mail):
        """Tests for sending capacity mail successfully"""
        send_capacity_mail("test_owner@example.com", "Test Body", "Test Subject")
        mock_send_mail.assert_called_once_with(
            "Test Subject",
            "Test Body",
            settings.EMAIL_HOST_USER,
            ["test_owner@example.com"]
        )

    @patch('request.views.send_mail', side_effect=ValueError)
    def test_send_capacity_mail_value_error(self, mock_send_mail):
        """Tests for sending capacity mail with ValueError"""
        with self.assertLogs(level='INFO') as log:
            send_capacity_mail("test_owner@example.com", "Test Body", "Test Subject")
            self.assertIn("failed to send mail due to error in body", log.output)

    @patch('request.views.send_mail', side_effect=Exception)
    def test_send_capacity_mail_generic_error(self, mock_send_mail):
        """Tests for sending capacity mail with generic exception"""
        with self.assertLogs(level='INFO') as log:
            send_capacity_mail("test_owner@example.com", "Test Body", "Test Subject")
            self.assertIn("failed to send mail", log.output)
