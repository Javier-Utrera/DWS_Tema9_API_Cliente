from django import forms
from .models import *
from datetime import *
from django.utils import timezone
from .helper import helper

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
#Necesito traerme los clientes y las estaciones

class CrearCita(forms.Form):
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
    
    fecha_matriculacion = forms.DateField(
    required=False,
    label="Fecha matriculacion",
    widget=forms.DateInput(
        format="%Y-%m-%d",
        attrs={"type": "date"},
        ),
    )
    
    numero_bastidor = forms.CharField(
        max_length=17,
        label="Número de Bastidor",
        required=False
    ) 
     
    tipo_inspeccion = forms.ChoiceField(
        required=False,
        label="Tipo de Inspección",
        choices=[('', 'Seleccione un tipo de inspección')] + TIPOINSPECCION,
    )
    remolque = forms.BooleanField(
        required=False,
        label="¿Tiene remolque?"
    )
    tipo_pago = forms.ChoiceField(
        choices=[("efectivo", "Efectivo"), ("tarjeta", "Tarjeta")],  # Ajusta según los valores reales
        label="Tipo de Pago"
    )     
    fecha_propuesta = forms.DateField(
        required=False,
        label="Fecha propuesta",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    hora_propuesta = forms.TimeField(
        widget=forms.TimeInput(attrs={'type': 'time'}),
        label="Hora Propuesta"
    )

def __init__(self, *args, **kwargs):
    super (CrearCita, self).__init__(*args,**kwargs)
    
    clientesDisponibles=helper.obtener_clientes_select()
    self.fields["cliente"] = forms.ChoiceField(
        choices=clientesDisponibles,
        widget=forms.Select,
        required=True,
    )
    estacionesDisponibles=helper.obtener_estaciones_select()
    self.fields["estacion"] = forms.ChoiceField(
        choices=estacionesDisponibles,
        widget=forms.Select,
        required=True,
    )