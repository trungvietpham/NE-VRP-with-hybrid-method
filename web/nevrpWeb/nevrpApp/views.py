from django.shortcuts import render
from django.http import HttpResponse
from .models import *

# Create your views here.

def home(request):
    context = {}
    return render(request, "nevrpApp/home.html", context)

def order(request):
    order = Order.objects.all()
    return render(request, "nevrpApp/order.html", {'order': order})

def node(request):
    node = Node.objects.all()
    return render(request, 'nevrpApp/node.html', {'node': node})

def vehicle(request):
    vehicle = Vehicle.objects.all()
    return render(request, 'nevrpApp/vehicle.html', {'vehicle': vehicle})

def order_result(request):
    data = Order.objects.values_list('code')
    return render(request, 'nevrpApp/order_result.html', {'order_result': data})

def search_order(request):
    data = 1 # Read from file
    code = request.POST['code']
    return render(request, 'nevrpApp/order_result.html', {"code": code, "res": 2})