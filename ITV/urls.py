from django.contrib.auth import views as auth_views
from django.urls import path
from django.contrib import admin
from .import views

urlpatterns = [
    path('', views.index,name="urls_index"),
    #Listar
    path('clientes/listar_clientes', views.api_listar_clientes,name="api_listar_clientes"),



    path('inspecciones/listar_inspecciones', views.api_listar_inspecciones,name="api_listar_inspecciones"), 
    
#-----------------------------------------------------------

    path('inspecciones/buscar',views.api_buscar_inspeccion,name="api_buscar_inspeccion"),


#-----------------------------------------------------------    

    path('citas/listar_citas', views.api_listar_citas,name="api_listar_citas"),
    path('citas/buscar',views.api_buscar_cita,name="api_buscar_cita"),
    path('citas/crear',views.api_crear_cita,name="api_crear_cita"),
    path('citas/editar/<int:cita_id>',views.api_editar_cita,name="api_editar_cita"),
    path('citas/actualizar/matricula/<int:cita_id>',views.api_cita_actualizar_matricula,name="api_cita_actualizar_matricula"),
    path('citas/eliminar/<int:cita_id>',views.api_eliminar_cita,name="api_eliminar_cita"),
    
#-----------------------------------------------------------

    path('locales/listar_locales', views.api_listar_locales, name="api_listar_locales"),
    path('locales/buscar', views.api_buscar_local, name="api_buscar_local"),
    path('locales/crear', views.api_crear_local, name="api_crear_local"),
    path('locales/editar/<int:local_id>', views.api_editar_local, name="api_editar_local"),
    path('locales/actualizar/duenio/<int:local_id>', views.api_actualizar_local_duenio, name="api_actualizar_local_duenio"),
    path('locales/eliminar/<int:local_id>', views.api_eliminar_local, name="api_eliminar_local"),

#-----------------------------------------------------------  

    path('trabajadores/listar_trabajadores', views.api_listar_trabajadores,name="api_listar_trabajadores"),
    path('trabajadores/buscar',views.api_buscar_trabajador,name="api_buscar_trabajador"),
    path('trabajadores/crear', views.api_crear_trabajador, name="api_crear_trabajador"),
    path('trabajadores/editar/<int:trabajador_id>', views.api_editar_trabajador, name="api_editar_trabajador"),
    path('trabajadores/actualizar/puesto/<int:trabajador_id>', views.api_actualizar_trabajador_puesto, name="api_actualizar_trabajador_puesto"),
    path('trabajadores/eliminar/<int:trabajador_id>', views.api_eliminar_trabajador, name="api_eliminar_trabajador"),

#-----------------------------------------------------------  

    path('vehiculos/listar_vehiculos', views.api_listar_vehiculos,name="api_listar_vehiculos"),
    path('vehiculos/buscar',views.api_buscar_vehiculo,name="api_buscar_vehiculo"),
    path('vehiculos/crear', views.api_crear_vehiculo, name="api_crear_vehiculo"),
    path('vehiculos/editar/<int:vehiculo_id>', views.api_editar_vehiculo, name="api_editar_vehiculo"),
    path('vehiculos/actualizar/matricula/<int:vehiculo_id>', views.api_actualizar_matricula_vehiculo, name="api_actualizar_matricula_vehiculo"),
    path('vehiculos/eliminar/<int:vehiculo_id>', views.api_eliminar_vehiculo, name="api_eliminar_vehiculo"),
    
#-------------------------------------------------------------
    #ViewSet
    path('locales_viewset/listar_locales', views.api_listar_locales_viewset, name="api_listar_locales_viewset"),
    path('locales_viewset/buscar', views.api_buscar_local_viewset, name="api_buscar_local_viewset"),
    path('locales_viewset/crear', views.api_crear_local_viewset, name="api_crear_local_viewset"),
    path('locales_viewset/editar/<int:local_id>', views.api_editar_local_viewset, name="api_editar_local_viewset"),
    path('locales_viewset/actualizar/duenio/<int:local_id>', views.api_actualizar_local_duenio_viewset, name="api_actualizar_local_duenio_viewset"),
    path('locales_viewset/eliminar/<int:local_id>', views.api_eliminar_local_viewset, name="api_eliminar_local_viewset"),
]