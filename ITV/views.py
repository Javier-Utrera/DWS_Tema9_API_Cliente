from urllib.error import HTTPError
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
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaCita(request.GET)       
        try:
            headers = crear_cabecera()
            response = requests.get(
                "http://127.0.0.1:8000/api/v1/citas/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                citas = response.json()
                return render(request, "citas/listar_citas.html",
                              {"views_citas":citas})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'citas/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaCita(None)
    return render(request, 'citas/busqueda_avanzada.html',{"formulario":formulario})

def api_buscar_inspeccion(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaInspeccion(request.GET)       
        try:
            headers = crear_cabecera()
            response = requests.get(
                "http://127.0.0.1:8000/api/v1/inspecciones/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                inspecciones = response.json()
                return render(request,"inspecciones/listar_inspecciones.html",{
                    "views_inspecciones_vehiculo":inspecciones})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'inspecciones/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaInspeccion(None)
    return render(request, 'inspecciones/busqueda_avanzada.html',{"formulario":formulario})

def api_buscar_vehiculo(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaVehiculo(request.GET)       
        try:
            headers = crear_cabecera()
            response = requests.get(
                "http://127.0.0.1:8000/api/v1/vehiculos/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                vehiculos = response.json()
                return render(request,"vehiculos/listar_vehiculos.html",{
                    "views_vehiculos":vehiculos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'vehiculos/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaVehiculo(None)
    return render(request, 'vehiculos/busqueda_avanzada.html',{"formulario":formulario})

def api_buscar_trabajador(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaTrabajador(request.GET)       
        try:
            headers = crear_cabecera()
            response = requests.get(
                "http://127.0.0.1:8000/api/v1/trabajadores/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                trabajadores = response.json()
                return render(request,"trabajadores/listar_trabajadores.html",{
                    "views_trabajadores_estacion":trabajadores})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'trabajadores/busqueda_avanzada.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaTrabajador(None)
    return render(request, 'trabajadores/busqueda_avanzada.html',{"formulario":formulario})