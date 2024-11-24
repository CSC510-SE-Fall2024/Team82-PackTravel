from django.test import TestCase
from ..forms import RideForm

class RideFormTest(TestCase):
    """Test class for the RideForm"""

    def test_ride_form_valid(self):
        """Tests for valid form submission"""
        form_data = {
            "source": "Raleigh, NC",
            "destination": "New York, NY",
        }
        form = RideForm(data=form_data)
        
        # Assert the form is valid
        self.assertTrue(form.is_valid())

    def test_ride_form_invalid(self):
        """Tests for invalid form submission"""
        form_data = {
            "source": "",  # Missing required field
            "destination": "New York, NY",
        }
        form = RideForm(data=form_data)
        
        # Assert the form is invalid
        self.assertFalse(form.is_valid())
        self.assertIn('source', form.errors)  # The 'source' field should have an error

    def test_ride_form_field_attributes(self):
        """Tests if form fields have the correct widget attributes"""
        form = RideForm()
        
        # Check 'source' field widget attributes
        self.assertEqual(form.fields['source'].widget.attrs['placeholder'], 'Enter your starting point here')
        self.assertEqual(form.fields['source'].widget.attrs['class'], 'form-control')

        # Check 'destination' field widget attributes
        self.assertEqual(form.fields['destination'].widget.attrs['placeholder'], 'Enter your destination here')
        self.assertEqual(form.fields['destination'].widget.attrs['class'], 'form-control')

