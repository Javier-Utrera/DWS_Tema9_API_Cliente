from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from .import views

urlpatterns = [
    path('', views.index,name="urls_index"),
    #Listar
    path('clientes/listar_clientes', views.api_listar_clientes,name="api_listar_clientes"),
    path('citas/listar_citas', views.api_listar_citas,name="api_listar_citas"),
    path('trabajadores/listar_trabajadores', views.api_listar_trabajadores,name="api_listar_trabajadores"),
    path('vehiculos/listar_vehiculos', views.api_listar_vehiculos,name="api_listar_vehiculos"),
    path('inspecciones/listar_inspecciones', views.api_listar_inspecciones,name="api_listar_inspecciones"), 
    
    #Buscar 
    path('citas/buscar',views.api_buscar_cita,name="api_buscar_cita"),
    path('inspecciones/buscar',views.api_buscar_inspeccion,name="api_buscar_inspeccion"),
    path('vehiculos/buscar',views.api_buscar_vehiculo,name="api_buscar_vehiculo"),
    path('trabajadores/buscar',views.api_buscar_trabajador,name="api_buscar_trabajador"),
    
    #Crear
    path('citas/crear',views.api_crear_cita,name="api_crear_cita"),    
]