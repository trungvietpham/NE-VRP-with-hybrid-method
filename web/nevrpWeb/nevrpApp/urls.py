from . import views
from django.urls import path

urlpatterns = [
    path("", views.home, name = "home"),
    path("order", views.order, name = "order"),
    path("node", views.node, name = "node"),
    path("vehicle", views.vehicle, name = "vehicle"),
    path("order_result", views.order_result, name="order_result"),
    path("order-search", views.search_order, name = "search-order"),
    # path("node_result", views.node_result, name="node_result"),
    # path("order-search", views.search_node, name = "search-node"),
    path("vehicle_result", views.vehicle_result, name="vehicle_result"),
    path("vehicle-search", views.search_vehicle, name = "search-vehicle"),
    
    
]
'''
    route: link to web url
    view: link to view func
    name: link to url in base.html
'''