import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

class helper:
    def obtener_clientes_select():
        headers = {'Authorization': 'Bearer '+env("Admin")}
        response = requests.get(
            env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/clientes/listar_clientes",
            headers=headers)
        clientes= response.json()
        lista_clientes=[("","Ninguna")]
        for cliente in clientes:
            lista_clientes.append((cliente["id"],cliente["nombre"]))
        return lista_clientes
    
    def obtener_estaciones_select():
        headers = {'Authorization': 'Bearer '+env("Admin")}
        response = requests.get(
            env('direccionservidorlocal')+"/api/"+env('VERSION_API')+"/estaciones/listar_estaciones",
            headers=headers)
        estaciones= response.json()
        lista_estaciones=[("","Ninguna")]
        for estacion in estaciones:
            lista_estaciones.append((estacion["id"],estacion["nombre"]))
        return lista_estaciones   