from django.http import HttpResponse, HttpResponseRedirect

from django.template.loader import get_template
from django.template import RequestContext, Context

from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout

from forms import *
from django.shortcuts import render_to_response
from models import Account

def logout_page(request):
    logout(request)
    return HttpResponseRedirect("/blog/")


def list_page(request):
    
       
    user_data = []
    for user in User.objects.all():
        acc = Account.objects.filter(owner=user.username)
        if acc:
    		user_data += [[ user,  acc[0]]]
        
    return render_to_response("list.html", {'user': request.user, 'user_data': user_data})
    return main_page(request)

def main_page(request):
        
    users = User.objects
    accounts = Account.objects.filter(owner=request.user.username)
    return render_to_response("main_page.html", {'user': request.user, 'accounts' : accounts, 'users': users})

def login_page(request): 
    if request.method == 'POST':
        form = FormularzLogowania(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password = form.cleaned_data['password'])
            login(request,user)
            template = get_template("main_page.html")
            variables = RequestContext(request,{'user':user})
            output = template.render(variables)
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
                template = get_template("main_page.html")
                variables = RequestContext(request,{'user':user})
                output = template.render(variables)
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