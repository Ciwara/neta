from django.contrib import admin

# Register your models here.


from .models import Owner, Vehicle, ModelVehicle, Made, AttachedFile


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'localite']
    list_filter = ['phone', 'localite']


class AttachedFileInline(admin.TabularInline):
    model = AttachedFile


class VehicleAdmin(admin.ModelAdmin):
    list_display = ['owner', 'model_vehicle', 'made',
                    'release_date', 'number', 'certify', 'lost', ]
    list_filter = ['owner', 'model_vehicle', 'certify', 'lost', 'made']
    inlines = [
        AttachedFileInline,
    ]


class ModelVehicleAdmin(admin.ModelAdmin):
    fields = ['model_vehicle', 'made', 'owner',
              'release_date', 'number', 'certify', 'lost', ]


class MadeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']
    pass


class AttachedFileAdmin(admin.ModelAdmin):
    list_display = ['doc', 'doc_type', 'vehicle', 'uploaded_at']
    pass

admin.site.register(Owner, OwnerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ModelVehicle, ModelVehicleAdmin)
admin.site.register(Made, MadeAdmin)
admin.site.register(AttachedFile, AttachedFileAdmin)
