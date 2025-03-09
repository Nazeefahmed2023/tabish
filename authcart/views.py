# from tokenize import generate_tokens
# from django.shortcuts import render,redirect,HttpResponse
# from django.contrib.auth.models import User
# from django.contrib import messages
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
# from django.views import View
# from .utils import TokenGenerator,generate_token
# from django.utils.encoding import force_str ,force_bytes ,DjangoUnicodeDecodeError
# from django.core.mail import EmailMessage 
# from django.conf import settings 
# # Create your views here.
# def signup(request):
#     if request.method=="POST":
#         email=request.POST['email']
#         password=request.POST['pass1']
#         confirm_password=request.POST['pass2']
#         if password != confirm_password:
#             messages.warning(request,'password is not matching')
#             return render(request,'signup.html')
#         try:
#             if User.objects.get(username=email):
#                 messages.info(request,'username is taken')
#                 return render(request,'signup.html')
#         except Exception as identifer:
#             pass
#         user= User.objects.create_user(email,email,password)
#         user.save()
#         email_subject="Activate your account"
#         message=render_to_string('activate.html',
#                 {
#                     'user':user,
#                     'domain':'127.0.0.1:8000',
#                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
#                     'token':generate_tokens.make_token(user)
#             } )
#         email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,[email],)
#         email_message.send()
#         message.success(request,"Activate your account by clicking the link in your gmail")
#         return redirect('/auth/login')
#         return HttpResponse("user created",email)
#     return render(request,"signup.html")
   
# class ActivateAccountView(View):
#     def get(self,request,uidb64,token):
#         try:
#             uid=force_str(urlsafe_base64_decode(uidb64))
#             user=user.objects.get(pk=uid)
#         except Exception as identifier:
#             user=None
#         if user is not None and generate_token.check_token(user,token):
#             user.is_active=True
#             user.save()
#             messages.info(request,"Account activated succesfully")
#             return redirect('/arkauth/login')
#         return render(request,'activatefail.html')













# def handlelogin(request):
#     return render(request,"login.html")
# def handlelogout(request):
#     return redirect('login.html')








from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from .utils import TokenGenerator, generate_token
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings


# Create your views here.
# def signup(request):
#     if request.method == "POST":
#         email = request.POST['email']
#         password = request.POST['pass1']
#         confirm_password = request.POST['pass2']
        
      
#         if password != confirm_password:
#             messages.warning(request, 'Passwords do not match')
#             return render(request, 'signup.html')

#         if User.objects.filter(username=email).exists():
#             messages.info(request, 'Username is already taken')
#             return render(request, 'signup.html')
        

#         user = User.objects.create_user(username=email, email=email, password=password)
#         user.is_active = False  
#         user.save()
        
     
#         email_subject = "Activate your account"
#         message = render_to_string('activate.html', {
#             'user': user,
#             'domain': '127.0.0.1:8000',
#             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#             'token': generate_token.make_token(user)  
#         })
#         email_message = EmailMessage(email_subject, message, settings.EMAIL_HOST_USER, [email])
#         email_message.send()
        
#         messages.success(request, "Activate your account by clicking the link in your email")
#         return redirect('/auth/login')
    
#     return render(request, "signup.html")

def signup(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['pass1']
        confirm_password = request.POST['pass2']
        
        # Check password confirmation
        if password != confirm_password:
            messages.warning(request, 'Passwords do not match')
            return render(request, 'signup.html')
        
        # Check if username (email) already exists
        if User.objects.filter(username=email).exists():
            messages.info(request, 'Username is already taken')
            return render(request, 'signup.html')
        
        # Create the user
        User.objects.create_user(username=email, email=email, password=password)
        messages.success(request, "Signup successful! Please log in.")
        
        # Redirect to login page
        return redirect('/auth/login')  # Or use reverse('login') if named URLs are set up
    
    return render(request, "signup.html")

class ActivateAccountView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None
        
        if user is not None and generate_token.check_token(user, token):  # Use generate_token here
            user.is_active = True
            user.save()
            messages.info(request, "Account activated successfully")
            return redirect('/auth/login')
        
        return render(request, 'activatefail.html')

def handlelogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pass1']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to the home or base page
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')  # Redirect back to login if authentication fails
    return render(request, "login.html")

def home(request):
    return render(request, 'index.html')
# def handlelogin(request):
#     return render(request, "login.html")


def handlelogout(request):
    return redirect('login')
