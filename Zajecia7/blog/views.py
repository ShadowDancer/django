# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect


from django.template.loader import get_template
from django.template import RequestContext, Context

from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

from forms import *
from django.shortcuts import render_to_response
from models import Account, Operation
from django.db.models import Q
import operator

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/blog/")

def transfer(userSource, userTarget, title, amount, admin):
    try:
        userSource_acc = Account.objects.filter(owner=userSource)
        if not userSource_acc:
            raise Exception(u"Nieznany użytkownik")
        userSource_acc = userSource_acc[0]
        
        
        
        
        userTarget_acc = Account.objects.filter(owner=userTarget)
        if not userTarget_acc:
            raise Exception(u"Nieznany użytkownik")
        userTarget_acc = userTarget_acc[0]
            
            
        if userSource == userTarget and admin != 1:
            raise Exception(u"Nie można przelewać na swoje konto!")
        
        if amount < 0 and admin != 1:
            raise Exception(u"Ujemna kwota przelewu!")
        
        if amount == 0:
            raise Exception("Kwota musi być różna od 0")
        
        if userSource_acc.balance < amount and admin != 1:
            raise Exception(u"Brak środków!")
            
        
        transfer_obj = Operation()
        transfer_obj.SourceAccount = userSource_acc
        transfer_obj.TargetAccount = userTarget_acc
        transfer_obj.title = title
        transfer_obj.amount = amount
        transfer_obj.save()
        userTarget_acc.balance += amount
        userTarget_acc.save()
        if admin != 1:
            userSource_acc = Account.objects.filter(owner=userSource)[0]
            userSource_acc.balance -= amount
            userSource_acc.save()
        return 'Ok'
    except Exception,e:
        return e
    
    

def redirect_page(request):
    return HttpResponseRedirect("/blog/list/")
    
def transfer_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/blog/login/")
    else:
        account = Account.objects.filter(owner=request.user.username)[0]
        
        error = ''
        if request.method == 'POST':
            if request.user.is_authenticated:
                add_owner = request.POST.get('owner')
                add_amount = request.POST.get('amount')
                add_account = Account.objects.filter(owner=add_owner)
                add_mode = 0
                add_title = request.POST.get('title')
                if request.POST.get('mode') == 'admin':
                    add_mode = 1
                if add_account:
                    add_account = add_account[0]
                    result = transfer(request.user.username, add_owner, add_title, int(add_amount), add_mode)
                    if result <> 'Ok':
                        error = result
            	else:
                	error = 'Nieznany użytkownik!'
                    
    	return render_to_response("transfer.html", {'user': request.user, 'account': account, 'error': error })
    
   
def list_page(request):
    error = ''
    if request.method == 'POST':
        if request.user.is_authenticated:
            add_owner = request.POST.get('owner')
            add_amount = request.POST.get('amount')
            add_account = Account.objects.filter(owner=add_owner)
            add_mode = 0
            add_title = request.POST.get('title')
            if request.POST.get('mode') == 'admin':
                add_mode = 1
            if add_account:
                add_account = add_account[0]
                result = transfer(request.user.username, add_owner, add_title, int(add_amount), add_mode)
                if result <> 'Ok':
                    error = result
            else:
                error = 'Nieznany użytkownik!'

    
    
    user_data = []
    for user in User.objects.all():
        acc = Account.objects.filter(owner=user.username)
        if acc:
    		user_data += [[ user,  acc[0]]]
        
    return render_to_response("list.html", {'user': request.user, 'user_data': user_data, 'error' : error})

def account_page(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/blog/login/")
    else:
        account = Account.objects.filter(owner=request.user.username)[0]
        operations = Operation.objects.filter(Q(SourceAccount=account) | Q(TargetAccount=account))
        operations = operations.order_by('-created')
        
        
        return render_to_response("account.html", {'user': request.user, 'account': account, 'operations': operations })
    
def login_page(request): 
    if request.method == 'POST':
        form = FormularzLogowania(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password'])
            login(request,user)
            return HttpResponseRedirect("/blog/")                         
    else: 
        form = FormularzLogowania()
    template = get_template("registration/login.html")    
    variables = RequestContext(request,{'form':form})
    output = template.render(variables)
    return HttpResponse(output)

def register_page(request):
    if request.method == 'POST':
        form = FormularzRejestracji(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
              username=form.cleaned_data['username'],
              password=form.cleaned_data['password1'],
            )
            user.save()
            acc = Account()
            acc.owner = user.username
            acc.balance = 0
            acc.save()
            
            if form.cleaned_data['log_on']:
                user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
                login(request,user) 
                return HttpResponseRedirect("/blog/") 
            else:    
                template = get_template("registration/register_success.html")
                variables = RequestContext(request,{'username':form.cleaned_data['username']})
                output = template.render(variables)
                return HttpResponse(output)            
    else:
        form = FormularzRejestracji()
    template = get_template("registration/register.html")    
    variables = RequestContext(request,{'form':form})
    output = template.render(variables)
    return HttpResponse(output)