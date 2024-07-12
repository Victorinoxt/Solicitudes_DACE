from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Estudiante
import re

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email', 'ano_ingreso', 'carrera', 'estado_solicitud', 'es_egresado']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'}),
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'ano_ingreso': forms.NumberInput(attrs={'class': 'form-control'}),
            'carrera': forms.TextInput(attrs={'class': 'form-control'}),
            'estado_solicitud': forms.Select(attrs={'class': 'form-control'}),
            'es_egresado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')
        if not re.match(r'^\d{11}$', telefono):
            raise forms.ValidationError('El teléfono debe tener 11 dígitos.')
        return telefono

    def clean_cedula(self):
        cedula = self.cleaned_data.get('cedula')
        if not re.match(r'^\d{8,10}$', cedula):
            raise forms.ValidationError('La cédula debe tener entre 8 y 10 dígitos.')
        return cedula

    def clean_ano_ingreso(self):
        ano_ingreso = self.cleaned_data.get('ano_ingreso')
        if ano_ingreso < 2000 or ano_ingreso > 2024:
            raise forms.ValidationError('El año de ingreso debe estar entre 2000 y 2024.')
        return ano_ingreso

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
            raise forms.ValidationError('El correo electrónico no es válido.')
        return email

class AuthenticationFormCustom(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
