import requests
from django.core import serializers
from django.shortcuts import redirect, render
from .forms import *

import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

def crear_cabecera():
    return {'Authorization': 'Bearer '+env('Admin')}

def index(request): 
    return render(request, 'index.html')
def mi_error_400(request,exception=None):
    return render(request,"errores/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errores/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errores/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errores/500.html",None,None,500)

def api_listar_vehiculos(request):   
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('Cliente')} 
        else:
            headers = {'Authorization': 'Bearer '+env('Trabajador')}
    else:
        headers = {'Authorization': 'Bearer '+env('Cliente')}        
    
    response = requests.get("https://frroga.pythonanywhere.com/api/v1/citas/listar_citas",headers=headers)
    vehiculos= response.json()
    return render(request,"vehiculos/listar_vehiculos.html",{'views_vehiculos':vehiculos})

def api_listar_citas(request):
    
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('Cliente')} 
        else:
            headers = {'Authorization': 'Bearer '+env('Trabajador')}
    else:
        headers = {'Authorization': 'Bearer '+env('Cliente')}       
    
    response = requests.get("https://frroga.pythonanywhere.com/api/v1/citas/listar_citas",headers=headers)
    citas= response.json()
    return render(request,"citas/listar_citas.html",{'views_citas':citas})

def api_listar_clientes(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('Cliente')} 
        else:
            headers = {'Authorization': 'Bearer '+env('Trabajador')}
    else:
        headers = {'Authorization': 'Bearer '+env('Admin')}     
    response = requests.get("https://frroga.pythonanywhere.com/api/v1/clientes/listar_clientes",headers=headers)
    clientes= response.json()
    return render(request,"clientes/listar_clientes.html",{'views_listar_cliente':clientes})

def api_listar_trabajadores(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('Cliente')} 
        else:
            headers = {'Authorization': 'Bearer '+env('Trabajador')}
    else:
        headers = {'Authorization': 'Bearer '+env('Admin')}     
    response = requests.get("https://frroga.pythonanywhere.com/api/v1/trabajadores/listar_trabajadores",headers=headers)
    trabajadores= response.json()
    return render(request,"trabajadores/listar_trabajadores.html",{'views_trabajadores_estacion':trabajadores})

def api_listar_inspecciones(request):
    if (request.user.is_anonymous==False):     
        if (request.user and request.user.rol == 1):       
            headers = {'Authorization': 'Bearer '+env('Admin')} 
        elif (request.user and request.user.rol == 2):
            headers = {'Authorization': 'Bearer '+env('Cliente')} 
        else:
            headers = {'Authorization': 'Bearer '+env('Trabajador')}
    else:
        headers = {'Authorization': 'Bearer '+env('Admin')}        
    response = requests.get("https://frroga.pythonanywhere.com/api/v1/inspecciones/listar_inspecciones",headers=headers)
    inspecciones= response.json()
    return render(request,"inspecciones/listar_inspecciones.html",{'views_inspecciones_vehiculo':inspecciones})

def api_buscar_cita(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaCita(request.GET)
        if formulario.is_valid():
            mensaje = "Se ha buscado con los siguientes criterios:\n"
            
            matriculav = formulario.cleaned_data.get("matricula")
            tipo_inspeccionv = formulario.cleaned_data.get("tipo_inspeccion")
            fecha_propuestav = formulario.cleaned_data.get("fecha_propuesta")
            
            
            if matriculav != "":
                citas = citas.filter(matricula__icontains=matriculav)
                mensaje += "Matrícula buscada: {matriculav}\n"
            if tipo_inspeccionv != "":
                citas = citas.filter(tipo_inspeccion=tipo_inspeccionv)
                mensaje += "Tipo de inspección buscado: {tipo_inspeccionv}\n"
            if fecha_propuestav is not None:
                citas = citas.filter(fecha_propuesta=fecha_propuestav)
                mensaje += "Fecha propuesta buscada: {fecha_propuestav.strftime('%d-%m-%Y')}\n"
            
            headers = crear_cabecera()
            response = requests.get(
                "https://frroga.pythonanywhere.com/api/v1/citas/api_buscar_cita",
                headers=headers,
                params=formulario.cleaned_data                           
            )
            citas=response.json()          
            return render(request, "citas/listar_citas.html", {
                "views_citas": citas,
                "texto_busqueda": mensaje,
            })
        if("HTTP_REFERER" in request.Meta):
            return redirect(request.META["HTTP_REFERER"])
        else:
            return redirect("index")
    else:
        formulario = BusquedaAvanzadaCita(None)
    
    return render(request, 'citas/busqueda_avanzada.html', {"formulario": formulario})