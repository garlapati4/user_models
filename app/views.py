from django.shortcuts import render
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    USFO=UserForm()
    PFO=ProfileModelForm()
    d={'USFO':USFO,'PFO':PFO}
    if request.method=='POST' and request.FILES:
        USFD=UserForm(request.POST)
        PFD=ProfileModelForm(request.POST,request.FILES)
        if USFD.is_valid() and PFD.is_valid():
            NSUFO=USFD.save(commit=False)
            submittedpassword=USFD.cleaned_data['password']
            NSUFO.set_password(submittedpassword)
            NSUFO.save()
            NSPO=PFO.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()
            

            send_mail('Registration',
                       'Registration is successful',
                        'garlapatinikhithachowdary@gmail.com',
                          [NSUFO.email],fail_silently=False)
            return HttpResponse('Registration is successful check in admin')

    return render(request,'registration.html',d)
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO:
            if AUO.is_active:
                login(request,AUO)
                request.session['username']=username
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse('Not a active user ')
        else:
            return HttpResponse('Invalid data')


    return render(request,'user_login.html')
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))