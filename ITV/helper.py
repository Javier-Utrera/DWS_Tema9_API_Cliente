from django.shortcuts import render
import requests
import environ
import os
from pathlib import Path
from django.contrib import messages
from django.shortcuts import redirect

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

class helper:

    def obtener_clientes_select():
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/clientes/listar_clientes"
        response = requests.get(url, headers=headers)
        clientes = response.json()
        lista_clientes = [("", "Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente["id"], cliente["nombre"]))
        return lista_clientes

    def obtener_estaciones_select():
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/estaciones/listar_estaciones"
        response = requests.get(url, headers=headers)
        estaciones = response.json()
        lista_estaciones = [("", "Ninguna")]
        for estacion in estaciones:
            lista_estaciones.append((estacion["id"], estacion["nombre"]))
        return lista_estaciones

    def obtener_cita(id):
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/citas/cita/" + str(id)
        response = requests.get(url, headers=headers)
        return response.json()

    def obtener_local(id):
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/locales/local/" + str(id)
        response = requests.get(url, headers=headers)
        return response.json()

    def obtener_trabajador(id):
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/trabajadores/trabajador/" + str(id)
        response = requests.get(url, headers=headers)
        return response.json()

    def obtener_trabajadores_select():
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/trabajadores/listar_trabajadores"
        response = requests.get(url, headers=headers)
        trabajadores = response.json()
        lista_trabajadores = [("", "Ninguno")]
        for trabajador in trabajadores:
            lista_trabajadores.append((trabajador["id"], trabajador["nombre"]))
        return lista_trabajadores

    def obtener_vehiculo(id):
        headers = {'Authorization': 'Bearer ' + env("Admin")}
        url = env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/vehiculos/vehiculo/" + str(id)
        response = requests.get(url, headers=headers)
        return response.json()

    def obtener_token_session(usuario,password):
        token_url = env('direccionservidorlocal')+'/oauth2/token/'
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'mi_aplicacion',
            'client_secret': 'mi_clave_secreta',
        }

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))
        

    # ejecuto la peticion y controlo los errores 
    @staticmethod
    def perform_request(method, url, headers=None, params=None, data=None):
        response = None
        try:
            method = method.lower()
            if method == "get":
                response = requests.get(url, headers=headers, params=params)
            elif method == "post":
                response = requests.post(url, headers=headers, data=data)
            elif method == "put":
                response = requests.put(url, headers=headers, data=data)
            elif method == "patch":
                response = requests.patch(url, headers=headers, data=data)
            elif method == "delete":
                response = requests.delete(url, headers=headers)
            else:
                raise ValueError(f"Método {method} no soportado")
            
            response.raise_for_status() 
            return {'success': True, 'response': response}
        
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error: {http_err}')
            return {
                'success': False,
                'error': http_err,
                'status': response.status_code if response is not None else None,
                'response': response
            }
        
        except requests.exceptions.RequestException as req_err:
            print(f'Request error: {req_err}')
            return {'success': False, 'error': req_err, 'status': None, 'response': None}
        
        except Exception as err:
            print(f'Unexpected error: {err}')
            return {'success': False, 'error': err, 'status': None, 'response': None}

    # construyo la URL base 
    @staticmethod
    def _build_url(endpoint):
        print("Servidor alojado en " + env('direccionservidorlocal'))
        return f"{env('direccionservidorlocal')}/api/{env('VERSION_API')}/{endpoint}"

    #  crear las cabeceras segun el usuario 
    @staticmethod
    def _crear_cabecera_por_usuario(request):
        
        token = request.session.get("token")

        if not token:
            raise Exception("No se encontró un token en la sesión. El usuario debe autenticarse.")

        return {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }

    # peticion, manejo de errores y respuesta.
    @staticmethod
    def api_request(request, method, endpoint, params=None, data=None, extra_headers=None):
        headers = helper._crear_cabecera_por_usuario(request)
        url = helper._build_url(endpoint)
        result = helper.perform_request(method, url, headers=headers, params=params, data=data)
        
        if result['success']:
            try:
                return result['response'].json()
            except Exception:
                return result['response'].text
        else:
            status = result.get('status')
            if status == 400:
                errors = {}
                if result['response'] is not None:
                    try:
                        errors = result['response'].json()
                    except Exception:
                        errors = {}
                return render(request, "errores/400.html", {"errores": errors}, status=400)
            elif status == 403:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                return redirect("urls_index")
            elif status == 404:
                return render(request, "errores/404.html", status=404)
            else:
                return render(request, "errores/500.html", status=500)

