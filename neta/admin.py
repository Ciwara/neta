# Register your models here.
from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import Owner, Vehicle, ModelVehicle, Made, AttachedFile


class UserCreationForm(forms.ModelForm):

    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Owner
        fields = ('email', 'date_of_birth')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = Owner
        fields = (
            'email', 'password', 'date_of_birth', 'is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'date_of_birth', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'date_of_birth', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# class OwnerAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'phone', 'localite']
#     list_filter = ['phone', 'localite']


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

# Now register the new UserAdmin...
admin.site.register(Owner, UserAdmin)
admin.site.unregister(Group)
# admin.site.register(Owner, OwnerAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(ModelVehicle, ModelVehicleAdmin)
admin.site.register(Made, MadeAdmin)
admin.site.register(AttachedFile, AttachedFileAdmin)
