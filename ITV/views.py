import requests
from django.core import serializers
from django.shortcuts import render

import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()
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
        headers = {"Authorization":"Bearer 7YfFXTXnKfIVBKBTghydsB6kdNCT9W"}       
    
    response = requests.get("http://127.0.0.1:8000/api/v1/citas/listar_citas",headers=headers)
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
        headers = {"Authorization":"Bearer 7YfFXTXnKfIVBKBTghydsB6kdNCT9W"}       
    
    response = requests.get("http://127.0.0.1:8000/api/v1/citas/listar_citas",headers=headers)
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
        headers = {"Authorization":"Bearer 7YfFXTXnKfIVBKBTghydsB6kdNCT9W"}     
    response = requests.get("http://127.0.0.1:8000/api/v1/clientes/listar_clientes",headers=headers)
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
        headers = {"Authorization":"Bearer 7YfFXTXnKfIVBKBTghydsB6kdNCT9W"}     
    response = requests.get("http://127.0.0.1:8000/api/v1/trabajadores/listar_trabajadores",headers=headers)
    trabajadores= response.json()
    return render(request,"trabajadores/listar_trabajadores.html",{'views_trabajadores_estacion':trabajadores})