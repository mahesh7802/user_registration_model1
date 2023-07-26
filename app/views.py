from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from app.models import *
from app.forms import *
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail

# Create your views here.



def registration(request):
    d={'usfo':UserForm,'pfo':ProfileForm}
    if request.method=='POST' and request.FILES:
        usfd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if usfd.is_valid() and pfd.is_valid():
            NSUFO=usfd.save(commit=False)
            submitedpw=usfd.cleaned_data['password']
            NSUFO.set_password(submitedpw)
            NSUFO.save()
            NSPO=pfd.save(commit=False)
            NSPO.username=NSUFO
            NSPO.save()

            send_mail('registration',
                      'you registration is sucessfully ',
                      'bandimahesh7802@gmail.com',
                      [NSUFO.email],
                      fail_silently=True)

            return HttpResponse('<center>Registration is successfully</center>')
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
                return HttpResponse('Not a Active User')
        else:
            return HttpResponse('Invalid Details')
    return render(request,'user_login.html')



@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))



@login_required
def display_details(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    
    return render(request,'display_details.html',d)



@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST.get('pw')
        un=request.session.get('username')
        UO=User.objects.get(username=un)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password chaged sucessfully')
    return render(request,'change_password.html')


def rest_password(request):
    if request.method=='POST':
        un=request.POST['un']
        pw=request.POST['pw']
        LUO=User.objects.filter(username=un)
        if LUO:
            UO=LUO[0]
            UO.set_password(pw)
            UO.save()
            return HttpResponse('password is done')
        else:
            return HttpResponse('invalid username')
    return render(request,'reset_password.html')