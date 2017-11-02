#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from neta.models import Vehicle
from neta.forms import LoginForm, SearchForm, UserCreationForm, AddVehicleForm


def init(request):

    search_form = SearchForm(request.POST or None)
    result = ""
    result_not_found = ""
    if request.method == 'POST' and '_search' in request.POST:
        print("search")
        if search_form.is_valid():
            result = search_form.get_result('number_engin')
            if not result:
                print("Not found")
                result_not_found = "Aucun numéro ne correspond"

    context = {'user': request.user, 'result_not_found': result_not_found,
               'search_form': search_form, 'msg_result': result,
               'settings': settings}
    return context


def add_user(request):
    pass


def index(request):

    context = init(request)
    login_form = LoginForm()
    new_user_form = UserCreationForm()
    if request.user.is_authenticated():
        return redirect("/home")

    if request.method == 'POST' and '_login' in request.POST:
        login_form = LoginForm(request.POST or None)
        print("login")
        if login_form.is_valid():
            user = login_form.login(request)
            if user:
                login(request, user)
                print('redirect')
                return redirect("/home")
    elif request.method == 'POST' and '_add_user' in request.POST:
        new_user_form = UserCreationForm(request.POST or None)
        print("add-user")
        if new_user_form.is_valid():
            new_user_form.save()
            user = new_user_form.login(request)

            # import ipdb; ipdb.set_trace()
            if user:
                login(request, user)
                return redirect("/home")
    context.update({'login_form': login_form,
                    'new_user_form': new_user_form})
    return render(request, 'index.html', context)


@login_required
def home(request):
    user = request.user
    if request.method == 'POST' and '_vehicle' in request.POST:
        add_vehicle_form = AddVehicleForm(request.POST or None)
        if add_vehicle_form.is_valid():
            print(add_vehicle_form)
            form = add_vehicle_form.save(commit=False)
            form.owner = user
            form.save()
            # add_vehicle_form.save()
            return redirect("/home")
    else:
        add_vehicle_form = AddVehicleForm()

    engins = Vehicle.objects.filter(owner=user)
    context = init(request)
    context.update({"engins": engins,
                    "add_vehicle_form": add_vehicle_form})
    return render(request, 'home.html', context)
