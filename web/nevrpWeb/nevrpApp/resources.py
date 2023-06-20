from import_export import resources
from .models import *
class NodeAdminResource(resources.ModelResource):
    class Meta: 
        model = Node
        exclude = ('id',)
        import_id_fields = ('code', )
        
class OrderAdminResource(resources.ModelResource):
    class Meta:
        model = Order
        exclude = ('id',)
        import_id_fields = ('code', )
        
class VehicleAdminResource(resources.ModelResource):
    class Meta: 
        model = Vehicle
        exclude = ('id',)
        import_id_fields = ('code', )