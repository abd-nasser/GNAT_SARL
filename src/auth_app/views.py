from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
import logging

from .forms import PersonnelRegisterForm, ChangeCredentialsForm
from .models import Personnel


logger = logging.getLogger(__name__)


def register_view(request):
    if request.method == "POST":
        
        try :
            form = PersonnelRegisterForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data["email"]
                
                #Generate username 
                first_three_letter = form.cleaned_data["first_name"][:3].lower() #first three letter of user first_name in lowercase
                all_last_name = form.cleaned_data["last_name"].lower().replace(" ", "")#all last_name in lowercase too
                base_username = f"{first_three_letter}_{all_last_name}"
                
                #Checks if the username is already in database 
                username = base_username
                counter = 1
                while Personnel.objects.filter(username=username).exists():
                    username = f'{base_username}{counter}'
                    counter += 1
                    
                #Generate password
                import secrets
                alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"   
                password = "".join(secrets.choice(alphabet) for _ in range(10))
                
                #create user personnel
                user = Personnel.objects.create(
                    username=username,
                    password=password,
                    first_name=form.cleaned_data["first_name"],
                    last_name=form.cleaned_data["last_name"],
                    email=form.cleaned_data["email"],
                    post=form.cleaned_data["post"],
                    telephone=form.cleaned_data["telephone"],
                    date_de_naissance=form.cleaned_data["date_de_naissance"],
                    lieu_de_naissance=form.cleaned_data["lieu_de_naissance"],
                    personne_a_prevenir=form.cleaned_data["personne_a_prevenir_en_cas"]              
                )
                
                send_mail(
                    subject="Identifiant Temporaire",
                    message=f"""Bonjour, Mr/Mme {form.cleaned_data.get('first_name')},
                    \n Vos identifiant pour GNAT sarl gestion sont les suivants : 
                    \n nom d'utilisateur = {username}
                    \n mot de passe = {password}
                    \n Ces informations sont à titre personnel,
                    \n Veuillez les garder en sécurité et privée
                    """ ,
                    from_email=settings.EMAIL_HOST_USER, #sender email defini at setting.py 
                    fail_silently=False,
                    recipient_list=[email]
                )
                
                messages.success(request, 
                    f"✅ {user.get_full_name()} inscrit(e)!\n"
                    f"👤 Login: {username}\n"
                    f"🔐 MDP: {password}")
                
        except Exception as e:
            logger.error(f"Erreur lors de l'inscription : {e}")
            messages.error(request, f"Erreur lors de l'inscription : {e}")
    else:
        form = PersonnelRegisterForm()
    return render(request, "modal/register.html", {"form": form})



def login_view(request):
    if request.method == "POST":
        
        try:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                
                #redirect each user to his interface according to his post
                if user.is_superuser and user.post.nom == "Directeur":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Directeur.")
                    return render(request, "directeur_templates/directeur.html")
                
                elif user.post.nom == "Comptable":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Comptable.")
                    return render(request, "comptable_templates/comptable.html")
                
                elif user.post.nom == "receptionniste":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Receptionniste.")
                    return render(request, "receptionniste_templates/receptionniste.html")
                
                elif user.post.nom == "chef d'atelier":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Chef d'Atelier.")
                    return render(request, "chef_atelier_templates/chef_atelier.html")
                
                elif user.post.nom == "laveur":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Laveur.")
                    return render(request, "laveur_templates/laveur.html")
                
                elif user.post.nom == "mecanicien":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Mecanicien.")
                    return render(request, "mecanicien_templates/mecanicien.html")
                
                elif user.post.nom == "peintre":
                    messages.success(request, f"Bienvenue {user.get_full_name()}! Vous êtes connecté en tant que Peintre.")
                    return render(request, "peintre_templates/peintre.html")
                else:
                    messages.error(request, "Poste non reconnu.")
        
        except Exception as e:
            logger.error(f"Erreur lors de la connexion : {e}")
            messages.error(request, f"Erreur lors de la connexion : {e}")
            