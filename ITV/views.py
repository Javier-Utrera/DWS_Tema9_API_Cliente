import json
from requests.exceptions import HTTPError, RequestException
import requests
from django.core import serializers
from django.shortcuts import redirect, render
from .forms import *
import environ
import os
from pathlib import Path
from django.contrib import messages
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()

def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + env('Admin'),
        'Content-Type': "application/json"
    }

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

#-----------------------------------------------------------


def api_listar_clientes(request):
    result = helper.api_request(request, "get", "clientes/listar_clientes")
    if hasattr(result, "status_code"):
        return result
    return render(request, "clientes/listar_clientes.html", {'views_listar_cliente': result})

def api_listar_inspecciones(request):
    result = helper.api_request(request, "get", "inspecciones/listar_inspecciones")
    if hasattr(result, "status_code"):
        return result
    return render(request, "inspecciones/listar_inspecciones.html", {'views_inspecciones_vehiculo': result})

def api_buscar_inspeccion(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaInspeccion(request.GET)
        result = helper.api_request(request, "get", "inspecciones/buscar", params=formulario.data)
        
        if hasattr(result, "status_code"):
            return result
        
        return render(request, "inspecciones/listar_inspecciones.html", {"views_inspecciones_vehiculo": result})
    
    else:
        formulario = BusquedaAvanzadaInspeccion(None)
    
    return render(request, "inspecciones/busqueda_avanzada.html", {"formulario": formulario})

#-----------------------------------------------------------

#Metodos refactorizados

def api_listar_locales(request):
    result = helper.api_request(request, "get", "locales/listar_locales")
    if hasattr(result, "status_code"):
        return result
    return render(request, "locales/listar_local.html", {'views_locales': result})

def api_buscar_local(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaLocal(request.GET)
        result = helper.api_request(request, "get", "locales/buscar", params=formulario.data)
        if hasattr(result, "status_code"):
            return result
        return render(request, "locales/listar_local.html", {"views_locales": result})
    else:
        formulario = BusquedaAvanzadaLocal(None)
    return render(request, 'locales/busqueda_avanzada.html', {"formulario": formulario})

def api_crear_local(request):
    if request.method == "POST":
        formulario = CrearLocal(request.POST)
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["anio_arrendamiento"] = str(
                datetime.date(
                    year=int(request.POST["anio_arrendamiento_year"]),
                    month=int(request.POST["anio_arrendamiento_month"]),
                    day=int(request.POST["anio_arrendamiento_day"])
                )
            )
            datos["metros"] = float(datos["metros"])
            result = helper.api_request(request, "post", "locales/crear", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales")
        else:
            return render(request, 'locales/create.html', {"formulario": formulario})
    else:
        formulario = CrearLocal(None)
    return render(request, 'locales/create.html', {"formulario": formulario})

def api_editar_local(request, local_id):
    local_data = helper.obtener_local(local_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CrearLocal(datosFormulario, initial={
        "precio": local_data["precio"],
        "metros": local_data["metros"],
        "anio_arrendamiento": local_data["anio_arrendamiento"],
        "duenio": local_data["duenio"]
    })
    if request.method == "POST":
        formulario = CrearLocal(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            datos["anio_arrendamiento"] = str(
                datetime.date(
                    year=int(request.POST["anio_arrendamiento_year"]),
                    month=int(request.POST["anio_arrendamiento_month"]),
                    day=int(request.POST["anio_arrendamiento_day"])
                )
            )
            datos["metros"] = float(datos["metros"])
            result = helper.api_request(request, "put", f"locales/editar/{local_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales")
        else:
            return render(request, "locales/actualizar.html", {"formulario": formulario})
    return render(request, "locales/actualizar.html", {
        "formulario": formulario,
        "local": local_data
    })

def api_actualizar_local_duenio(request, local_id):
    local_data = helper.obtener_local(local_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = LocalActualizarDuenioForm(datosFormulario, initial={"duenio": local_data["duenio"]})
    if request.method == "POST":
        formulario = LocalActualizarDuenioForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            result = helper.api_request(request, "patch", f"locales/actualizar/duenio/{local_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales")
        else:
            return render(request, "locales/actualizar_duenio.html", {"formulario": formulario, "local": local_data})
    return render(request, "locales/actualizar_duenio.html", {
        "formulario": formulario,
        "local": local_data
    })

def api_eliminar_local(request, local_id):
    result = helper.api_request(request, "delete", f"locales/eliminar/{local_id}")
    # con hasattr veo si result tiene el atributo status_code, si lo tiene es que viene con error
    if hasattr(result, "status_code"):
        return result
    messages.success(request, result)
    return redirect("api_listar_locales")

#-----------------------------------------------------------

#Metodos refactorizados

def api_listar_citas(request):
    result = helper.api_request(request, "get", "citas/listar_citas")
    if hasattr(result, "status_code"):
        return result
    return render(request, "citas/listar_citas.html", {'views_citas': result})

def api_buscar_cita(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaCita(request.GET)
        result = helper.api_request(request, "get", "citas/buscar", params=formulario.data)
        if hasattr(result, "status_code"):
            return result
        return render(request, "citas/listar_citas.html", {"views_citas": result})
    else:
        formulario = BusquedaAvanzadaCita(None)
    return render(request, 'citas/busqueda_avanzada.html', {"formulario": formulario})

def api_crear_cita(request):
    if request.method == "POST":
        formulario = CrearCita(request.POST)
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["fecha_matriculacion"] = str(
                datetime.date(
                    year=int(datos['fecha_matriculacion_year']),
                    month=int(datos['fecha_matriculacion_month']),
                    day=int(datos['fecha_matriculacion_day'])
                )
            )
            datos["fecha_propuesta"] = str(
                datetime.date(
                    year=int(datos['fecha_propuesta_year']),
                    month=int(datos['fecha_propuesta_month']),
                    day=int(datos['fecha_propuesta_day'])
                )
            )
            result = helper.api_request(request, "post", "citas/crear", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_citas")
        else:
            return render(request, 'citas/create.html', {"formulario": formulario})
    else:
        formulario = CrearCita(None)
    return render(request, 'citas/create.html', {"formulario": formulario})

def api_editar_cita(request, cita_id):
    cita_data = helper.obtener_cita(cita_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CrearCita(datosFormulario, initial={
        "cliente": cita_data["cliente"]["id"],
        "estacion": cita_data["estacion"]["id"],
        "matricula": cita_data["matricula"],
        "fecha_matriculacion": datetime.datetime.strptime(cita_data["fecha_matriculacion"], "%Y-%m-%d").date(),
        "numero_bastidor": cita_data["numero_bastidor"],
        "tipo_inspeccion": cita_data["tipo_inspeccion"],
        "remolque": cita_data["remolque"],
        "tipo_pago": cita_data["tipo_pago"],
        "fecha_propuesta": datetime.datetime.strptime(cita_data["fecha_propuesta"], "%Y-%m-%d").date(),
        "hora_propuesta": cita_data["hora_propuesta"]
    })
    if request.method == "POST":
        formulario = CrearCita(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            datos["fecha_matriculacion"] = str(datetime.date(
                year=int(request.POST["fecha_matriculacion_year"]),
                month=int(request.POST["fecha_matriculacion_month"]),
                day=int(request.POST["fecha_matriculacion_day"])
            ))
            datos["fecha_propuesta"] = str(datetime.date(
                year=int(request.POST["fecha_propuesta_year"]),
                month=int(request.POST["fecha_propuesta_month"]),
                day=int(request.POST["fecha_propuesta_day"])
            ))
            datos["hora_propuesta"] = str(formulario.cleaned_data["hora_propuesta"])
            result = helper.api_request(request, "put", f"citas/editar/{cita_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_citas")
        else:
            return render(request, "citas/actualizar.html", {"formulario": formulario})
    return render(request, "citas/actualizar.html", {
        "formulario": formulario,
        "cita": cita_data
    })

def api_cita_actualizar_matricula(request, cita_id):
    cita_data = helper.obtener_cita(cita_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CitaActualizarMatriculaForm(datosFormulario, initial={"matricula": cita_data["matricula"]})
    if request.method == "POST":
        formulario = CitaActualizarMatriculaForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            result = helper.api_request(request, "patch", f"citas/actualizar/matricula/{cita_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_citas")
        else:
            return render(request, "citas/actualizar_matricula.html", {"formulario": formulario, "cita": cita_data})
    return render(request, "citas/actualizar_matricula.html", {
        "formulario": formulario,
        "cita": cita_data
    })

def api_eliminar_cita(request, cita_id):
    result = helper.api_request(request, "delete", f"citas/eliminar/{cita_id}")
    if hasattr(result, "status_code"):
        return result
    messages.success(request, result)
    return redirect("api_listar_citas")

#-----------------------------------------------------------

#Metodos refactorizados

def api_listar_trabajadores(request):
    result = helper.api_request(request, "get", "trabajadores/listar_trabajadores")
    if hasattr(result, "status_code"):
        return result
    return render(request, "trabajadores/listar_trabajadores.html", {'views_trabajadores_estacion': result})

def api_buscar_trabajador(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaTrabajador(request.GET)
        result = helper.api_request(request, "get", "trabajadores/buscar", params=formulario.data)
        if hasattr(result, "status_code"):
            return result
        return render(request, "trabajadores/listar_trabajadores.html", {"views_trabajadores_estacion": result})
    else:
        formulario = BusquedaAvanzadaTrabajador(None)
    return render(request, 'trabajadores/busqueda_avanzada.html', {"formulario": formulario})

def api_crear_trabajador(request):
    if request.method == "POST":
        formulario = CrearTrabajador(request.POST)
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["estacion"] = request.POST.getlist("estacion")
            result = helper.api_request(request, "post", "trabajadores/crear", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_trabajadores")
        else:
            return render(request, "trabajadores/create.html", {"formulario": formulario})
    else:
        formulario = CrearTrabajador(None)
    return render(request, "trabajadores/create.html", {"formulario": formulario})

def api_editar_trabajador(request, trabajador_id):
    trabajador_data = helper.obtener_trabajador(trabajador_id)
    estaciones_disponibles = helper.obtener_estaciones_select()
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CrearTrabajador(datosFormulario, initial={
        "email": trabajador_data["email"],
        "nombre": trabajador_data["nombre"],
        "apellidos": trabajador_data["apellidos"],
        "puesto": trabajador_data["puesto"],
        "sueldo": trabajador_data["sueldo"],
        "observaciones": trabajador_data["observaciones"],
        "estacion": [estacion["id"] for estacion in trabajador_data["estacion"]]
    })
    if request.method == "POST":
        formulario = CrearTrabajador(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            datos["estacion"] = request.POST.getlist("estacion")
            result = helper.api_request(request, "put", f"trabajadores/editar/{trabajador_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_trabajadores")
        else:
            return render(request, "trabajadores/actualizar.html", {
                "formulario": formulario,
                "trabajador": trabajador_data,
                "estaciones": estaciones_disponibles
            })
    return render(request, "trabajadores/actualizar.html", {
        "formulario": formulario,
        "trabajador": trabajador_data,
        "estaciones": estaciones_disponibles
    })

def api_actualizar_trabajador_puesto(request, trabajador_id):
    trabajador_data = helper.obtener_trabajador(trabajador_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = TrabajadorActualizarPuestoForm(datosFormulario, initial={"puesto": trabajador_data["puesto"]})
    if request.method == "POST":
        formulario = TrabajadorActualizarPuestoForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            result = helper.api_request(request, "patch", f"trabajadores/actualizar/puesto/{trabajador_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_trabajadores")
        else:
            return render(request, "trabajadores/actualizar_puesto.html", {"formulario": formulario, "trabajador": trabajador_data})
    return render(request, "trabajadores/actualizar_puesto.html", {"formulario": formulario, "trabajador": trabajador_data})

def api_eliminar_trabajador(request, trabajador_id):
    result = helper.api_request(request, "delete", f"trabajadores/eliminar/{trabajador_id}")
    if hasattr(result, "status_code"):
        return result
    messages.success(request, result)
    return redirect("api_listar_trabajadores")

#-----------------------------------------------------------

#Metodos refactorizados

def api_listar_vehiculos(request):
    result = helper.api_request(request, "get", "vehiculos/listar_vehiculos")
    if hasattr(result, "status_code"):
        return result
    return render(request, "vehiculos/listar_vehiculos.html", {'views_vehiculos': result})

def api_buscar_vehiculo(request):
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaVehiculo(request.GET)
        result = helper.api_request(request, "get", "vehiculos/buscar", params=formulario.data)
        if hasattr(result, "status_code"):
            return result
        return render(request, "vehiculos/listar_vehiculos.html", {"views_vehiculos": result})
    else:
        formulario = BusquedaAvanzadaVehiculo(None)
    return render(request, 'vehiculos/busqueda_avanzada.html', {"formulario": formulario})

def api_crear_vehiculo(request):
    if request.method == "POST":
        formulario = CrearVehiculo(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            datos["trabajadores"] = json.loads(request.POST["trabajadores"])
            datos["fecha_matriculacion"] = str(
                datetime.date(
                    year=int(datos['fecha_matriculacion_year']),
                    month=int(datos['fecha_matriculacion_month']),
                    day=int(datos['fecha_matriculacion_day'])
                )
            )
            result = helper.api_request(request, "post", "vehiculos/crear", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, "Vehículo creado correctamente")
            return redirect("api_listar_vehiculos")
        else:
            return render(request, "vehiculos/create.html", {"formulario": formulario})
    else:
        formulario = CrearVehiculo()
    return render(request, "vehiculos/create.html", {"formulario": formulario})

def api_editar_vehiculo(request, vehiculo_id):
    vehiculo_data = helper.obtener_vehiculo(vehiculo_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CrearVehiculo(datosFormulario, initial={
        "marca": vehiculo_data["marca"],
        "modelo": vehiculo_data["modelo"],
        "numero_bastidor": vehiculo_data["numero_bastidor"],
        "tipo_vehiculo": vehiculo_data["tipo_vehiculo"],
        "cilindrada": vehiculo_data["cilindrada"],
        "potencia": vehiculo_data["potencia"],
        "combustible": vehiculo_data["combustible"],
        "mma": vehiculo_data["mma"],
        "asientos": vehiculo_data["asientos"],
        "ejes": vehiculo_data["ejes"],
        "dni_propietario": vehiculo_data["dni_propietario"],
        "matricula": vehiculo_data["matricula"],
        "fecha_matriculacion": vehiculo_data["fecha_matriculacion"],
        "trabajadores": [trabajador["id"] for trabajador in vehiculo_data["trabajadores"]]
    })
    if request.method == "POST":
        formulario = CrearVehiculo(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            datos["trabajadores"] = list(map(int, request.POST.getlist("trabajadores")))
            datos["fecha_matriculacion"] = str(
                datetime.date(
                    year=int(request.POST["fecha_matriculacion_year"]),
                    month=int(request.POST["fecha_matriculacion_month"]),
                    day=int(request.POST["fecha_matriculacion_day"])
                )
            )
            result = helper.api_request(request, "put", f"vehiculos/editar/{vehiculo_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_vehiculos")
        else:
            return render(request, "vehiculos/actualizar.html", {"formulario": formulario, "vehiculo": vehiculo_data})
    return render(request, "vehiculos/actualizar.html", {"formulario": formulario, "vehiculo": vehiculo_data})

def api_actualizar_matricula_vehiculo(request, vehiculo_id):
    vehiculo_data = helper.obtener_vehiculo(vehiculo_id)
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = VehiculoActualizarMatriculaForm(datosFormulario, initial={"matricula": vehiculo_data["matricula"]})
    if request.method == "POST":
        formulario = VehiculoActualizarMatriculaForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            result = helper.api_request(request, "patch", f"vehiculos/actualizar/matricula/{vehiculo_id}", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_vehiculos")
        else:
            return render(request, "vehiculos/actualizar_matricula.html", {"formulario": formulario, "vehiculo": vehiculo_data})
    return render(request, "vehiculos/actualizar_matricula.html", {"formulario": formulario, "vehiculo": vehiculo_data})

def api_eliminar_vehiculo(request, vehiculo_id):
    result = helper.api_request(request, "delete", f"vehiculos/eliminar/{vehiculo_id}")
    if hasattr(result, "status_code"):
        return result
    messages.success(request, result)
    return redirect("api_listar_vehiculos")

#-----------------------------------------------------------

#CRUD ViewSet
def api_listar_locales_viewset(request):
    result = helper.api_request(request, "get", "locales/")
    if hasattr(result, "status_code"):
        return result
    return render(request, "locales/listar_local.html", {'views_locales': result})

def api_buscar_local_viewset(request):
    # Si deseas búsqueda con filtros, puedes enviar parámetros a /locales/
    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaLocal(request.GET)
        result = helper.api_request(request, "get", "locales/", params=formulario.data)
        if hasattr(result, "status_code"):
            return result
        return render(request, "locales/listar_local.html", {"views_locales": result})
    else:
        formulario = BusquedaAvanzadaLocal(None)
    return render(request, 'locales/busqueda_avanzada.html', {"formulario": formulario})

def api_crear_local_viewset(request):
    if request.method == "POST":
        formulario = CrearLocal(request.POST)
        if formulario.is_valid():
            datos = formulario.data.copy()
            datos["anio_arrendamiento"] = str(
                datetime.date(
                    year=int(request.POST["anio_arrendamiento_year"]),
                    month=int(request.POST["anio_arrendamiento_month"]),
                    day=int(request.POST["anio_arrendamiento_day"])
                )
            )
            datos["metros"] = float(datos["metros"])
            # Endpoint del ViewSet para crear es /locales/
            result = helper.api_request(request, "post", "locales/", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales_viewset")
        else:
            return render(request, 'locales/create.html', {"formulario": formulario})
    else:
        formulario = CrearLocal(None)
    return render(request, 'locales/create.html', {"formulario": formulario})

def api_editar_local_viewset(request, local_id):
    # Primero obtenemos el local usando GET en el endpoint /locales/<local_id>/
    local_data = helper.api_request(request, "get", f"locales/{local_id}/")
    if hasattr(local_data, "status_code"):
        return local_data
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = CrearLocal(datosFormulario, initial={
        "precio": local_data["precio"],
        "metros": local_data["metros"],
        "anio_arrendamiento": local_data["anio_arrendamiento"],
        "duenio": local_data["duenio"]
    })
    if request.method == "POST":
        formulario = CrearLocal(request.POST)
        if formulario.is_valid():
            datos = formulario.cleaned_data.copy()
            datos["anio_arrendamiento"] = str(
                datetime.date(
                    year=int(request.POST["anio_arrendamiento_year"]),
                    month=int(request.POST["anio_arrendamiento_month"]),
                    day=int(request.POST["anio_arrendamiento_day"])
                )
            )
            datos["metros"] = float(datos["metros"])
            # Endpoint para actualizar (PUT) es /locales/<local_id>/
            result = helper.api_request(request, "put", f"locales/{local_id}/", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales_viewset")
        else:
            return render(request, "locales/actualizar.html", {"formulario": formulario})
    return render(request, "locales/actualizar.html", {
        "formulario": formulario,
        "local": local_data
    })

def api_actualizar_local_duenio_viewset(request, local_id):
    # Para actualizar parcialmente (por ejemplo, solo el campo 'duenio')
    local_data = helper.api_request(request, "get", f"locales/{local_id}/")
    if hasattr(local_data, "status_code"):
        return local_data
    datosFormulario = request.POST if request.method == "POST" else None
    formulario = LocalActualizarDuenioForm(datosFormulario, initial={"duenio": local_data["duenio"]})
    if request.method == "POST":
        formulario = LocalActualizarDuenioForm(request.POST)
        if formulario.is_valid():
            datos = request.POST.copy()
            # Endpoint para actualización parcial (PATCH) es /locales/<local_id>/
            result = helper.api_request(request, "patch", f"locales/{local_id}/", data=json.dumps(datos))
            if hasattr(result, "status_code"):
                return result
            messages.success(request, result)
            return redirect("api_listar_locales_viewset")
        else:
            return render(request, "locales/actualizar_duenio.html", {"formulario": formulario, "local": local_data})
    return render(request, "locales/actualizar_duenio.html", {
        "formulario": formulario,
        "local": local_data
    })

def api_eliminar_local_viewset(request, local_id):
    # Endpoint para eliminar es /locales/<local_id>/
    result = helper.api_request(request, "delete", f"locales/{local_id}/")
    if hasattr(result, "status_code"):
        return result
    messages.success(request, result)
    return redirect("api_listar_locales_viewset")

#-----------------------------------------------------------

#Registro
def api_registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                datos = request.POST.copy()
                
                fecha_nacimiento = datos.get("fecha_nacimiento", None)
                if fecha_nacimiento:
                    try:
                        fecha_nacimiento = datetime.datetime.strptime(fecha_nacimiento, "%d-%m-%Y").strftime("%Y-%m-%d")
                        datos["fecha_nacimiento"] = fecha_nacimiento
                    except ValueError:
                        formulario.add_error("fecha_nacimiento", "Formato de fecha inválido")  
                                   
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    env('direccionservidorlocal') + "/api/" + env('VERSION_API') + "/registrar/usuario",
                    headers=headers,
                    data=json.dumps(datos)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"] = usuario
                    request.session["token"] = token_acceso
                    return redirect("urls_index")
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
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def api_login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get( env('direccionservidorlocal') +'/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            print(usuario)
            request.session["usuario"] = usuario
            
            return redirect("urls_index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})

def api_logout(request):
    del request.session['token']
    return redirect('urls_index')