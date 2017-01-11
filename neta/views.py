#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.contrib.auth import login

from neta.forms import LoginForm


def index(request):
    form = LoginForm(request.POST or None)
    if request.POST and form.is_valid():
        user = form.login(request)
        if user:
            login(request, user)
            return redirect("/home")  # Redirect to a success page.
    return render(request, 'index.html', {'login_form': form})


@login_required
def home(request):
    context = {'user': request.user}
    return render(request, 'home.html', context)
