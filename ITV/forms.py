from django import forms
from .models import *
from datetime import *
from django.utils import timezone

class BusquedaAvanzadaCita(forms.Form):
    matricula = forms.CharField(
        required=False,
        label="Matrícula del vehículo",
        max_length=7,
    )
    tipo_inspeccion = forms.ChoiceField(
        required=False,
        label="Tipo de Inspección",
        choices=[('', 'Seleccione un tipo de inspección')] + Cita.TIPOINSPECCION,
    )
    fecha_propuesta = forms.DateField(
        required=False,
        label="Fecha propuesta",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    
    def clean(self):
        super().clean()
        
        matricula = self.cleaned_data.get("matricula")
        tipo_inspeccion = self.cleaned_data.get("tipo_inspeccion")
        fecha_propuesta = self.cleaned_data.get("fecha_propuesta")
        
        # Validación para que al menos un campo esté lleno
        if not matricula and not tipo_inspeccion and not fecha_propuesta:
            self.add_error("matricula","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("tipo_inspeccion","Debe introducir al menos un valor en un campo del formulario")
            self.add_error("fecha_propuesta","Debe introducir al menos un valor en un campo del formulario")
        
        # Validación de longitud de matrícula
        if matricula and len(matricula) > 7:
            self.add_error("matricula", "La matrícula no puede tener más de 7 caracteres.")
        
        # Validación de fecha futura
        if fecha_propuesta and fecha_propuesta < timezone.now().date():
            self.add_error("fecha_propuesta", "La fecha propuesta no puede ser una fecha pasada.")
        
        return self.cleaned_data