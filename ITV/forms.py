from django import forms
from .models import *
from datetime import *
from django.utils import timezone
from .helper import helper
import datetime
from django.contrib.auth.forms import UserCreationForm

#-----------------------------------------------------------
    
class BusquedaAvanzadaInspeccion(forms.Form):
    
    resultado_inspeccion=forms.CharField(required=False,label="Resultado de la inspeccion")
    notas_inspeccion=forms.CharField(required=False,label="Notas de la inspeccion")
    fecha_inspeccion=forms.DateField(required=False,label="Fecha de la inspeccion",
                                     widget=forms.DateInput(format="%Y-%m-%d", 
                                                            attrs={"type": "date"},))
       
#-----------------------------------------------------------

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
    
class CrearCita(forms.Form):
    TIPOINSPECCION=[
        ('PE','Periodica'),
        ('NOPE','NoPeriodica'),
        ('VETAX','VerificacionTaximetro'),
        ('VETAXV','VerificacionTaximetroCambioVehiculo')
    ]
    
    matricula = forms.CharField(
        required=True,
        label="Matrícula del vehículo",
        max_length=10,
    )
    
    fecha_matriculacion = forms.DateField(label="Fecha Matriculación",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget(years=range(1970,2026))
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
        choices=[("EF", "Efectivo"), ("TA", "Tarjeta")],
        label="Tipo de Pago"
    )     
    fecha_propuesta = forms.DateField(label="Fecha Propuesta",
                                        initial=datetime.date.today,
                                        widget= forms.SelectDateWidget(years=range(2025,2028))
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
            required=False,
        )
        
class CitaActualizarMatriculaForm(forms.Form):
    matricula = forms.CharField(
        required=True,
        label="Matrícula del vehículo",
        max_length=10,
        help_text="10 caracteres como máximo"
    )

#-----------------------------------------------------------

class BusquedaAvanzadaLocal(forms.Form):
    precio = forms.DecimalField(
        required=False,
        label="Precio del alquiler (€)",
        max_digits=10,
        decimal_places=2
    )
    
    metros = forms.DecimalField(
        required=False,
        label="Metros cuadrados",
        max_digits=10,
        decimal_places=3
    )

    anio_arrendamiento = forms.DateField(
        required=False,
        label="Año de arrendamiento",
        widget=forms.DateInput(
            format="%Y-%m-%d",
            attrs={"type": "date"},
        ),
    )
    
class CrearLocal(forms.Form):
    precio = forms.FloatField(
        required=True,
        label="Precio del alquiler (€)",
        min_value=0
    )

    metros = forms.DecimalField(
        required=True,
        label="Metros cuadrados",
        max_digits=50,
        decimal_places=3
    )

    anio_arrendamiento = forms.DateField(
        required=True,
        label="Año de arrendamiento",
        initial=datetime.date.today,
        widget=forms.SelectDateWidget(years=range(1950, 2030))
    )

    duenio = forms.CharField(
        required=True,
        label="Dueño del local",
        max_length=50
    )

class LocalActualizarDuenioForm(forms.Form):
    duenio = forms.CharField(
        required=True,
        label="Nuevo dueño del local",
        max_length=50
    )

#-----------------------------------------------------------

class BusquedaAvanzadaTrabajador(forms.Form):
    
    nombre=forms.CharField(required=False,label="Nombre")
    sueldo=forms.FloatField(required=False,label="Sueldo")
    puesto=forms.CharField(required=False,label="Puesto")

class CrearTrabajador(forms.Form):
    TIPO=[('',''),('EM','Emisiones'),('FR','Frenos'),('DI','Direccion')]
    nombre = forms.CharField(
        required=True,
        label="Nombre",
        max_length=50
    )

    apellidos = forms.CharField(
        required=False,
        label="Apellidos",
        max_length=50
    )

    email = forms.EmailField(
        required=True,
        label="Correo Electrónico"
    )

    puesto = forms.ChoiceField(
        required=True,
        label="Puesto",
        choices=[('', 'Seleccione un puesto')] + TIPO
    )

    sueldo = forms.FloatField(
        required=True,
        label="Sueldo (€)",
        min_value=0
    )

    observaciones = forms.CharField(
        required=False,
        label="Observaciones",
        widget=forms.Textarea(attrs={'rows': 3})
    )

    estacion = forms.MultipleChoiceField(
        required=True,
        label="Estaciones Asignadas",
        widget=forms.SelectMultiple
    )

    def __init__(self, *args, **kwargs):
        super(CrearTrabajador, self).__init__(*args, **kwargs)

        estacionesDisponibles = helper.obtener_estaciones_select()
        self.fields["estacion"] = forms.MultipleChoiceField(
            choices=estacionesDisponibles,
            widget=forms.SelectMultiple,
            required=False,
            label="Estaciones"
        )

class TrabajadorActualizarPuestoForm(forms.Form):
    TIPO=[('',''),('EM','Emisiones'),('FR','Frenos'),('DI','Direccion')]
    puesto = forms.ChoiceField(
        required=True,
        label="Nuevo Puesto",
        choices=[('', 'Seleccione un puesto')] +TIPO
    )

#-----------------------------------------------------------

class BusquedaAvanzadaVehiculo(forms.Form):
    
    marca=forms.CharField(required=False,label="Marca")
    potencia=forms.IntegerField(required=False,label="Potencia")
    matricula=forms.CharField(required=False,label="Matricula")
 
class CrearVehiculo(forms.Form):
    marca = forms.CharField(
        required=True,
        label="Marca",
        max_length=50
    )
    
    modelo = forms.CharField(
        required=True,
        label="Modelo",
        max_length=50
    )

    numero_bastidor = forms.CharField(
        required=True,
        label="Número de Bastidor",
        max_length=17
    )
    
    TIPO_VEHICULO = [
        ('tur', 'Turismo'),
        ('moto', 'Motocicleta'),
        ('cam', 'Camión'),
        ('bus', 'Autobús'),
        ('furg', 'Furgoneta'),
        ('quad', 'Quad'),
        ('tracto', 'Tractor')
    ]
    tipo_vehiculo = forms.ChoiceField(
        required=True,
        label="Tipo de Vehículo",
        choices=TIPO_VEHICULO
    )

    cilindrada = forms.IntegerField(
        required=True,
        label="Cilindrada"
    )

    potencia = forms.IntegerField(
        required=True,
        label="Potencia"
    )

    COMBUSTIBLE_CHOICES = [
        ('gas', 'Gasolina'),
        ('die', 'Diésel'),
        ('ele', 'Eléctrico'),
        ('hib', 'Híbrido'),
        ('gpl', 'GLP (Gas Licuado)'),
        ('gnv', 'GNC (Gas Natural)')
    ]
    combustible = forms.ChoiceField(
        required=True,
        label="Combustible",
        choices=COMBUSTIBLE_CHOICES
    )

    mma = forms.IntegerField(
        required=True,
        label="Masa Máxima Autorizada"
    )

    asientos = forms.IntegerField(
        required=True,
        label="Número de Asientos"
    )

    ejes = forms.IntegerField(
        required=True,
        label="Número de Ejes"
    )

    dni_propietario = forms.CharField(
        required=True,
        label="DNI del Propietario",
        max_length=9
    )

    matricula = forms.CharField(
        required=True,
        label="Matrícula",
        max_length=7
    )

    fecha_matriculacion = forms.DateField(
        required=True,
        label="Fecha de Matriculación",
        widget=forms.SelectDateWidget(years=range(1980, 2035))
    )

    trabajadores = forms.MultipleChoiceField(
        choices=helper.obtener_trabajadores_select(),
        widget=forms.SelectMultiple,
        required=True
    )
    
class VehiculoActualizarMatriculaForm(forms.Form):
    matricula = forms.CharField(
        required=True,
        label="Nueva Matrícula",
        max_length=7
    )
    
#-----------------------------------------------------------

class RegistroForm(UserCreationForm):
    roles = (
        (0,"Seleccione un tipo de rol"),
        (2,"cliente"),
        (3,"trabajador")        
    )
    
    rol= forms.ChoiceField(choices=roles)
    
    fecha_nacimiento = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'format': '%Y-%m-%d'})  
    )
    
    apellidos=forms.CharField(required=False)
    dni=forms.CharField(required=False)
       
    tipo=(('',''),('EM','Emisiones'),('FR','Frenos'),('DI','Direccion'))
    puesto=forms.ChoiceField(choices=tipo,required=False)    
    
    class Meta:
        model = Usuario
        fields = ('username','email','password1','password2','rol')
        
class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    
#-----------------------------------------------------------

class CrearCitaCliente(forms.Form):
    TIPOINSPECCION = [
        ('PE', 'Periodica'),
        ('NOPE', 'No Periodica'),
        ('VETAX', 'Verificacion Taximetro'),
        ('VETAXV', 'Verificacion Taximetro Cambio Vehiculo')
    ]

    matricula = forms.CharField(label="Matrícula", max_length=10)
    fecha_matriculacion = forms.DateField(label="Fecha Matriculación", widget=forms.SelectDateWidget(years=range(1970, 2026)))
    numero_bastidor = forms.CharField(label="Número de Bastidor", max_length=17, required=False)
    tipo_inspeccion = forms.ChoiceField(label="Tipo de Inspección", choices=TIPOINSPECCION)
    remolque = forms.BooleanField(label="¿Tiene remolque?", required=False)
    tipo_pago = forms.ChoiceField(label="Tipo de Pago", choices=[("EF", "Efectivo"), ("TA", "Tarjeta")])
    fecha_propuesta = forms.DateField(label="Fecha Propuesta", widget=forms.SelectDateWidget(years=range(2025, 2028)))
    hora_propuesta = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), label="Hora Propuesta")
    estacion = forms.ChoiceField(label="Estación ITV", choices=[])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        estacionesDisponibles = helper.obtener_estaciones_select()
        self.fields["estacion"].choices = estacionesDisponibles
        
class CrearVehiculoCliente(forms.Form):
    marca = forms.CharField(label="Marca", max_length=50)
    modelo = forms.CharField(label="Modelo", max_length=50)
    numero_bastidor = forms.CharField(label="Número de Bastidor", max_length=17)
    tipo_vehiculo = forms.ChoiceField(label="Tipo de Vehículo", choices=[('tur', 'Turismo'), ('moto', 'Motocicleta')])
    cilindrada = forms.IntegerField(label="Cilindrada")
    potencia = forms.IntegerField(label="Potencia")
    combustible = forms.ChoiceField(label="Combustible", choices=[('gas', 'Gasolina'), ('die', 'Diésel')])
    mma = forms.IntegerField(label="Masa Máxima Autorizada")
    asientos = forms.IntegerField(label="Número de Asientos")
    ejes = forms.IntegerField(label="Número de Ejes")
    matricula = forms.CharField(label="Matrícula", max_length=7)
    fecha_matriculacion = forms.DateField(label="Fecha de Matriculación", widget=forms.SelectDateWidget(years=range(1980, 2035)))