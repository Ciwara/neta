#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login
from django.conf import settings

from neta.forms import LoginForm, SearchForm


def init(request):

    search_form = SearchForm(request.POST or None)
    result = ""
    result_not_found = ""
    if request.POST and search_form.is_valid():
        result = search_form.get_result('number_engin')
        print(result)
        if not result:
            print("Not found")
            result_not_found = "Aucun numéro ne correspond"

    context = {'user': request.user, 'result_not_found': result_not_found,
               'search_form': search_form,
               'msg_result': result, 'settings': settings}
    return context


def index(request):

    context = init(request)
    login_form = LoginForm(request.POST or None)
    if request.POST and login_form.is_valid():
        user = login_form.login(request)
        if user:
            login(request, user)
            return redirect("/home")
    context.update({'login_form': login_form, })
    return render(request, 'index.html', context)


@login_required
def home(request):
    context = init(request)
    return render(request, 'home.html', context)
