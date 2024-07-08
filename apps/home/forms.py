from django import forms
from .models import Estudiante
import re

class EstudianteForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['nombre', 'apellido', 'cedula', 'telefono', 'email', 'ano_ingreso', 'carrera', 'estado_solicitud', 'es_egresado']

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
