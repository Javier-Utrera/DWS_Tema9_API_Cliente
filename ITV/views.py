import json
from requests.exceptions import HTTPError, RequestException
import requests
from django.core import serializers
from django.shortcuts import redirect, render
from .forms import *
import xmltodict
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

# Diccionario de formatos según la versión de la API
FORMATOS_POR_VERSION = {
    "v1": "json",
    "v2": "xml"
}

# Obtener el formato de respuesta basado en la versión de la API
FORMATO_RESPUESTA = FORMATOS_POR_VERSION.get(env('VERSION_API'), "json")

def crear_cabecera():

    formatos = {
        "json": "application/json",
        "xml": "application/xml"
    }
    
    # Siempre enviamos JSON, pero `Accept` depende de `FORMATO_RESPUESTA`
    return {
        'Authorization': 'Bearer ' + env('Admin'),
        'Content-Type': "application/json",  # Siempre enviamos JSON
        "Accept": formatos.get(FORMATO_RESPUESTA, "application/json")  # Dependiendo de la versión
    }

def obtener_parseador(response):
    content_type = response.headers.get("Content-Type", "").lower()
    if "application/json" in content_type:
        return response.json
    elif "application/xml" in content_type or "text/xml" in content_type:
        return lambda: json.loads(json.dumps(xmltodict.parse(response.text)))
    else:
        raise ValueError(f"Formato de respuesta desconocido: {content_type}")

def manejar_errores(request, response, formulario, template):
    try:
        response.raise_for_status()
    
    except HTTPError as http_err:
        print(f'Hubo un error en la petición: {http_err}')

        if response.status_code == 400:
            errores = response.json()           
            for error in errores:
                formulario.add_error(error,errores[error])

            return render(
                request, 
                template,
                {"formulario": formulario, "errores": errores}
            )

        else:
            return mi_error_500(request)
    
    except RequestException as req_err:
        print(f'Error de conexión: {req_err}')
        return mi_error_500(request)
    
    except Exception as err:
        print(f'Ocurrió un error inesperado: {err}')
        return mi_error_500(request)

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
                env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/citas/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                citas = obtener_parseador(response)()
                return render(request, "citas/listar_citas.html",
                              {"views_citas":citas})
        
            return manejar_errores(request, response, formulario, "citas/busqueda_avanzada.html")
        
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
                env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/inspecciones/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                inspecciones = obtener_parseador(response)()
                return render(request,"inspecciones/listar_inspecciones.html",{
                    "views_inspecciones_vehiculo":inspecciones})

            return manejar_errores(request, response, formulario, "inspecciones/busqueda_avanzada.html")
        
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
                env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/vehiculos/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                vehiculos = obtener_parseador(response)()
                return render(request,"vehiculos/listar_vehiculos.html",{
                    "views_vehiculos":vehiculos})
            
            return manejar_errores(request, response, formulario, "vehiculos/busqueda_avanzada.html")
        
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
                env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/trabajadores/buscar",
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                trabajadores = obtener_parseador(response)()
                return render(request,"trabajadores/listar_trabajadores.html",{
                    "views_trabajadores_estacion":trabajadores})
            
            return manejar_errores(request, response, formulario, "trabajadores/busqueda_avanzada.html")
        
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaTrabajador(None)
    return render(request, 'trabajadores/busqueda_avanzada.html',{"formulario":formulario})

def api_crear_cita(request):
    if(request.method == "POST"):
        try:
            formulario = CrearCita(request.POST)
            headers=crear_cabecera()
            datos=formulario.data.copy()
            
            datos["fecha_matriculacion"] = str(
                                            datetime.date(year=int(datos['fecha_publicacion_year']),
                                                        month=int(datos['fecha_publicacion_month']),
                                                        day=int(datos['fecha_publicacion_day']))
                                             )
            datos["fecha_propuesta"] = str(
                                            datetime.date(year=int(datos['fecha_publicacion_year']),
                                                        month=int(datos['fecha_publicacion_month']),
                                                        day=int(datos['fecha_publicacion_day']))
                                             )             
            response = request.post(
                env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"citas/crear",
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                return redirect("citas/listar_citas")
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
                            'citas/create.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = CrearCita(None)
    return render(request, 'citas/create.html',{"formulario":formulario})
            
            
        