from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from .import views

urlpatterns = [
    path('', views.index,name="urls_index"),
    #1
    path('clientes/listar_clientes', views.api_listar_clientes,name="api_listar_clientes"),
    
    #2
    path('citas/listar_citas', views.api_listar_citas,name="api_listar_citas"),
    
    #3
    path('trabajadores/listar_trabajadores', views.api_listar_trabajadores,name="api_listar_trabajadores"),
    
    #4
    path('vehiculos/listar_vehiculos', views.api_listar_vehiculos,name="api_listar_vehiculos"),
    
    #5
    path('inspecciones/listar_inspecciones', views.api_listar_inspecciones,name="api_listar_inspecciones"), 
    
    #Buscar cita  
    path('citas/buscar',views.api_buscar_cita,name="api_buscar_cita"),
]