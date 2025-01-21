import requests
from django.core import serializers
from django.shortcuts import render
def mi_error_400(request,exception=None):
    return render(request,"errores/400.html",None,None,400)

def mi_error_403(request,exception=None):
    return render(request,"errores/403.html",None,None,403)

def mi_error_404(request,exception=None):
    return render(request,"errores/404.html",None,None,404)

def mi_error_500(request,exception=None):
    return render(request,"errores/500.html",None,None,500)

def citas_lista_api(request):
    response = requests.get("http://127.0.0.1:8000/api/v1/citas")
    citas= response.json()
    return render(request,"citas/listar_citas.html",{'views_citas':citas})