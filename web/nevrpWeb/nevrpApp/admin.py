from django.contrib import admin
from .models import *
from .resources import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

class NodeAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = NodeAdminResource
admin.site.register(Node, NodeAdmin)

class OrderAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = OrderAdminResource
admin.site.register(Order, OrderAdmin)

class VehicleAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    resource_class = VehicleAdminResource
admin.site.register(Vehicle, VehicleAdmin)
