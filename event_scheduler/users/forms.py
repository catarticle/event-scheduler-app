from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from .models import User, THEME_CHOICES
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=False)
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    interests = forms.MultipleChoiceField(
        choices=THEME_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        label='Какие мероприятия вас интересуют?',
        required=False
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'first_name', 'last_name', 
                 'password1', 'password2', 'interests']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.add_interests_to_bio()
        if commit:
            user.save()
            user.interests = self.cleaned_data['interests']  # Это уже список
            user.save()
        
        return user

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Этот email уже используется.")
        return email

class UserUpdateForm(UserChangeForm):
    password = None  # Скрываем поле пароля
    
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Телефон должен быть в формате: '+999999999'. Максимум 15 цифр."
    )
    
    phone = forms.CharField(
        max_length=20,
        required=False,
        validators=[phone_validator],
        widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 
                 'phone', 'bio', 'birth_date']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['birth_date'].required = False
        self.fields['bio'].required = False
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("Этот email уже используется.")
        return email