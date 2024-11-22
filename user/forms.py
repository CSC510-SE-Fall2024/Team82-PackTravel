"""Django form definition for user"""
from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    """Form for user registration, including username, name, email, password, and phone number."""
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter a username', 'class': 'form-control'})
    )
    first_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-control'})
    )
    last_name = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-control'})
    )
    email = forms.EmailField(
        required=True, 
        max_length=60, 
        widget=forms.EmailInput(attrs={'placeholder': 'abc@mail.com', 'class': 'form-control'})
    )
    password1 = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )
    phone_number = forms.CharField(
        required=True, 
        max_length=11, 
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'phone_number')

class LoginForm(forms.ModelForm):
    """Form for user login, including username and password fields."""
    username = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username', 'class': 'form-control'})
    )
    password = forms.CharField(
        required=True, 
        widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('username', 'password')

class ProfileForm(forms.ModelForm):
    """Form for user profile, including travel preferences, likes, and smoker status."""
    travel_preferences = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your travel preferences', 'class': 'form-control'})
    )
    likes = forms.CharField(
        max_length=255, 
        required=True, 
        widget=forms.TextInput(attrs={'placeholder': 'Enter your likes (comma separated)', 'class': 'form-control'})
    )
    is_smoker = forms.BooleanField(
        required=False, 
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}), 
        label='Do you smoke?'
    )
    travel_with_pets = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Do you want a pet friendly ride?'
    )
    driver_gender = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label="More comfortable with a female driver?(This does not guarantee your driver's gender)"
    )

    class Meta:
        model = User
        fields = ('travel_preferences', 'likes', 'is_smoker', 'travel_with_pets', 'driver_gender')

class FeedbackForm(forms.Form):
    """Form for ride feedback, including ratings and textual feedback."""
    ride_rating = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Rate the ride (1-5)', 'class': 'form-control'})
    )
    driver_rating = forms.IntegerField(
        required=True,
        min_value=1,
        max_value=5,
        widget=forms.NumberInput(attrs={'placeholder': 'Rate the driver (1-5)', 'class': 'form-control'})
    )
    feedback = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'placeholder': 'Share your experience...', 'class': 'form-control', 'rows': 4})
    )

    class Meta:
        model = User
        fields = ('ride_rating', 'driver_rating', 'feedback')
