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

def api_listar_citas(request):
    headers = {"Authorization":"Bearer UTQYVQOHx8I1pjkz9K4csvzLuKW2Jl"}
    response = requests.get("http://127.0.0.1:8000/api/v1/citas/listar_citas",headers=headers)
    citas= response.json()
    return render(request,"citas/listar_citas.html",{'views_citas':citas})

def api_listar_clientes(request):
    headers = {"Authorization":"Bearer UTQYVQOHx8I1pjkz9K4csvzLuKW2Jl"}
    response = requests.get("http://127.0.0.1:8000/api/v1/clientes/listar_clientes",headers=headers)
    clientes= response.json()
    return render(request,"clientes/listar_clientes.html",{'views_listar_cliente':clientes})