from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from .models import CustomeUser
import datetime
from .utils import send_email_with_html_body
# Create your views here.
def home(request):
    return render(request,'index.html')

def register(request):
    if request.method=='POST':
        nom = request.POST.get('nom')
        prenom = request.POST.get('prenom')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password1 = request.POST.get('password1')

        user = CustomeUser.objects.filter(email=email)
        if user.exists():
            messages.error(request,'Cet email a un compte veuillez essayer avec un autre email.')
            return redirect('register')
        if password!=password1:
            messages.error(request,'Le deux mot de passe ne corresponde pas.')
        else:
            CustomeUser.objects.create_user(email=email,password=password,first_name=nom,last_name=prenom)
            subject = "Merci d'avoir créé votre compte"
            receivers = [email]
            template = 'email.html'
            context = {
                'email':email
            }
            has_send = send_email_with_html_body(subject=subject, receivers=receivers, template=template, context=context)
            if has_send:
                messages.success(request, 'Compte créé avec succès. Un email de confirmation a été envoyé.')
            else:
                messages.warning(request, 'Compte créé, mais échec de l\'envoi de l\'email.')
                
            return redirect('home')
    return render(request,'register.html')

def loginn(request):
    if request.method=='POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = CustomeUser.objects.filter(email=email)
        if user.exists():
            user = authenticate(email=email,password=password)
            print(user)
            if user is not None:
                messages.success(request,'Vous etes connecte avec succese')
                login(request,user)
                return redirect('home')
            else:
                messages.error(request,'Oups un probleme est survenue')
        else:
            messages.error(request,'User n\'exist pas')
    return render(request,'login.html')

def logoute(request):
    '''
        function to logout for user login 
    '''
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Disconnected...')
        return redirect('home')
    else:
        messages.error(request,'User is not connected...')