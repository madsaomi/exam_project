from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field', 'placeholder': 'Password'}),
        min_length=8,
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'field', 'placeholder': 'Confirm password'}),
        label='Confirm password',
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'field', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'field', 'placeholder': 'Email address'}),
        }

    def clean(self):
        cleaned = super().clean()
        if cleaned.get('password') != cleaned.get('password2'):
            raise forms.ValidationError('Passwords do not match')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
