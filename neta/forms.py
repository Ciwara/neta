#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django import forms
# from django.contrib.admin import widgets
from django.contrib.auth import authenticate
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from neta.models import Owner, Vehicle


class AddVehicleForm(forms.ModelForm):
    """docstring for ClassName"""

    class Meta:
        model = Vehicle
        exclude = ['owner', 'certify']
        widgets = {
            'number': forms.TextInput(attrs={
                'placeholder': "numero chassi"}),
            'release_date': forms.DateTimeInput(attrs={
                'class': 'datetimepicker'}),
            'lost': forms.CheckboxInput(attrs={
                'placeholder': "Perdu"}),
        }


class SearchForm(forms.Form):

    number_engin = forms.CharField(
        label="Numéro de l'engins", max_length=200, required=True,
        widget=forms.TextInput(attrs={'placeholder': 'recherche par numéro'}),)

    def get_result(self, required):
        try:
            result = Vehicle.objects.get(
                number=self.cleaned_data.get('number_engin'))
        except Exception:
            result = None
        return result


class LoginForm(forms.Form):
    phone = forms.CharField(max_length=255, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(phone=phone, password=password)

        if not isinstance(phone, int):
            try:
                phone = int(phone)
                print("int conv")
            except Exception as e:
                print(e)
                raise forms.ValidationError("Is not int.")
        if not user or not user.is_active:
            raise forms.ValidationError(
                "Sorry, that login was invalid. Please try again.")
        return self.cleaned_data

    def login(self, request):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(phone=phone, password=password)
        return user


class UserCreationForm(forms.ModelForm):
    """ A form for creating new users. Includes all the required fields, plus a
        repeated password.
    """

    class Meta:
        model = Owner
        fields = ('phone', 'date_of_birth', 'full_name', 'localite')
        exclude = ['email']

        widgets = {
            # 'date_of_birth': forms.DateInput(attrs={'class': 'datepicker'}),
            'full_name': forms.TextInput(attrs={
                'placeholder': "Nom et prénom"}),
            'localite': forms.TextInput(attrs={
                'placeholder': "Adresse"}),
            'date_of_birth': forms.TextInput(
                attrs={'placeholder': "Date", 'class': 'datepicker'}),
        }

    phone = forms.CharField(max_length=255, required=True)
    full_name = forms.CharField(max_length=200)
    date_of_birth = forms.DateField(label="Date de naissance")
    localite = forms.CharField(max_length=100)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    def login(self, request):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = authenticate(phone=phone, password=password)
        return user

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
        print(user)
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):

    """
        A form for updating users. Includes all the fields on
        the user, but replaces the password field with admin's
        password hash display field.
    """

    class Meta:
        model = Owner
        fields = ('phone', 'password', 'date_of_birth',
                  'full_name', 'localite')

    password = ReadOnlyPasswordHashField()

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
