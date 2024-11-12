from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate
from django.core.mail import send_mail
from .models import CustomeUser,CountryVisit
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
            user = CustomeUser.objects.create_user(email=email,password=password,first_name=nom,last_name=prenom)
            user.is_active = False
            user.save()
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


# pip install django-ipware,requests

# import requests
# from ipware import get_client_ip
# from django.http import JsonResponse
# from .models import CountryVisit

# def get_country_from_ip(ip_address):
#     # Remplace par ta clé API ipstack
#     api_key = 'YOUR_IPSTACK_API_KEY'
#     url = f"http://api.ipstack.com/{ip_address}?access_key={api_key}"
#     response = requests.get(url)
#     data = response.json()
#     return data.get('country_name', 'Unknown')

# def count_visit(request):
#     ip_address, is_routable = get_client_ip(request)
#     if ip_address is None:
#         ip_address = '0.0.0.0'  # IP par défaut si non disponible

#     country = get_country_from_ip(ip_address)

#     if country:
#         visit, created = CountryVisit.objects.get_or_create(country=country)
#         visit.visits += 1
#         visit.save()

#     return JsonResponse({'status': 'success', 'country': country})


# def home(request):
#     count_visit(request)  # Appelle la fonction pour compter la visite
#     visits = CountryVisit.objects.all()
#     return render(request, 'home.html', {'visits': visits})
