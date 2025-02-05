from django import forms
from .models import *
from datetime import *
from django.utils import timezone

class BusquedaAvanzadaCita(forms.Form):
    TIPOINSPECCION=[
        ('PE','Periodica'),
        ('NOPE','NoPeriodica'),
        ('VETAX','VerificacionTaximetro'),
        ('VETAXV','VerificacionTaximetroCambioVehiculo')
    ]
    matricula = forms.CharField(
        required=False,
        label="Matrícula del vehículo",
        max_length=7,
    )
    tipo_inspeccion = forms.ChoiceField(
        required=False,
        label="Tipo de Inspección",
        choices=[('', 'Seleccione un tipo de inspección')] + TIPOINSPECCION,
    )
    fecha_propuesta = forms.DateField(
        required=False,
        label="Fecha propuesta",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    
class BusquedaAvanzadaInspeccion(forms.Form):
    
    resultado_inspeccion=forms.CharField(required=False,label="Resultado de la inspeccion")
    notas_inspeccion=forms.CharField(required=False,label="Notas de la inspeccion")
    fecha_inspeccion=forms.DateField(required=False,label="Fecha de la inspeccion",
                                     widget=forms.DateInput(format="%Y-%m-%d", 
                                                            attrs={"type": "date"},))
    
class BusquedaAvanzadaVehiculo(forms.Form):
    
    marca=forms.CharField(required=False,label="Marca")
    potencia=forms.IntegerField(required=False,label="Potencia")
    matricula=forms.CharField(required=False,label="Matricula")
    
class BusquedaAvanzadaTrabajador(forms.Form):
    
    nombre=forms.CharField(required=False,label="Nombre")
    sueldo=forms.FloatField(required=False,label="Sueldo")
    puesto=forms.CharField(required=False,label="Puesto")