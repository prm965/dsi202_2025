from django import forms
from django.contrib.auth.models import User

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {
            'first_name': 'ชื่อ',
            'last_name': 'นามสกุล',
            'email': 'อีเมล'
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'input-field'}),
            'last_name': forms.TextInput(attrs={'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'class': 'input-field'}),
        }


from .models import UserProfile

PROFILE_CHOICES = [
    ('images/profile/avatar1.png', 'Avatar 1'),
    ('images/profile/avatar2.png', 'Avatar 2'),
    ('images/profile/avatar3.png', 'Avatar 3'),
    ('images/profile/avatar4.png', 'Avatar 4'),
]


class ProfileUpdateForm(forms.ModelForm):
    profile_image = forms.ChoiceField(
        choices=PROFILE_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
