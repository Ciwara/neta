
# Register your models here.
# from django import forms
from django.contrib import admin
# from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserChangeForm, UserCreationForm

from .models import AttachedFile, Made, ModelVehicle, Owner, Vehicle


class UserAdmin(BaseUserAdmin):

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('phone', 'full_name', 'email', 'date_of_birth',
                    'is_active', 'is_admin', 'localite')
    list_filter = ('is_active', 'localite')
    fieldsets = (
        ("Identifiant", {'fields': ('phone', 'email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'full_name',)}),
        ('Permissions', {'fields': ('is_admin', 'is_active', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'full_name', 'email', 'date_of_birth',
                       'password1', 'password2')}
         ),
        ('Permissions', {'fields': ('groups', 'is_admin')}),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class OwnerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'localite']
    list_filter = ['phone', 'localite']


class AttachedFileInline(admin.TabularInline):

    model = AttachedFile


class VehicleAdmin(admin.ModelAdmin):

    list_display = ['owner', 'model_vehicle',
                    'release_date', 'number', 'certify', 'lost', ]
    list_filter = [
                    # 'owner',
                    'model_vehicle', 'certify', 'lost']
    inlines = [
        AttachedFileInline,
    ]


class ModelVehicleAdmin(admin.ModelAdmin):
    # fields = ['model_vehicle', 'made', 'owner',
    #           'release_date', 'number', 'certify', 'lost', ]
    pass


class MadeAdmin(admin.ModelAdmin):
    list_display = ['name', 'country']


class AttachedFileAdmin(admin.ModelAdmin):

    list_display = ['doc', 'doc_type', 'vehicle', 'uploaded_at']

# Now register the new UserAdmin...
admin.site.register(Owner, UserAdmin)
# admin.site.unregister(Group)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ModelVehicle, ModelVehicleAdmin)
admin.site.register(Made, MadeAdmin)
admin.site.register(AttachedFile, AttachedFileAdmin)
