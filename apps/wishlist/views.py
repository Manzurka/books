# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    return render(request,'wishlist/index.html')

def validate(request):
    errors = User.objects.validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')
    else:
        user=User.objects.create(name=request.POST['name'],username=request.POST['username'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
        request.session ['name'] = request.POST['name']
        request.session ['id'] = user.id
        return redirect('/dashboard')

def login(request):
    errors = User.objects.login_validation(request.POST)
    if errors:
        if errors['login']  =="Successfully logged in!":
            user=User.objects.filter(username=request.POST['username'])
            request.session ['name'] = user[0].name
            request.session ['id'] = user[0].id
            return redirect('/dashboard')
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

def showall(request):
    return render(request,'wishlist/dashboard.html', {"items": Item.objects.all(), "liked_items" : User.objects.get(id=request.session['id']).liked_items.all()})

def showitem(request, id):
    return render(request,'wishlist/item.html', {"item": Item.objects.get(id=id), "users" : Item.objects.get(id=id).users.all()})

def remove(request, id):
    User.objects.get(id=request.session['id']).liked_items.remove(Item.objects.get(id=id))
    return redirect('/dashboard')

def delete(request, id):
    Item.objects.get(id=id).delete()
    return redirect('/dashboard')

def add(request, id):
    user=User.objects.get(id=request.session['id'])
    mywish = Item.objects.get(id=id)
    if mywish != user.liked_items:
        user.liked_items.add(mywish)
        print user.liked_items.all()
        return redirect('/dashboard')
    else:
        HttpResponse="This item is already in your wishlist"
        return redirect('/dashboard', HttpResponse)

def create(request):
    return render(request, 'wishlist/create.html')

def submit(request):
    errors = Item.objects.item_validation(request.POST)
    if errors:
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/create')
    else:
        creator=User.objects.get(id = request.session['id'])
        Item.objects.create(item_name=request.POST['item_name'], creator=creator)
        return redirect('/dashboard')
