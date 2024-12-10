from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from todo.models import UserImg
# Create your views here.
def login_user(request):
    if request.method == "POST":
        email = request.POST['userEmail']
        pswd = request.POST['userPswd']
        user = authenticate(request, username=email, password=pswd)

        if user is not None:
            login(request, user)
            return redirect("todo:listSelect")
        else:
            message = "The username/password entered is incorrect. Please try again."
            return render(request, 'authenticate/login.html', {'message': message})
    else:
        return render(request, 'authenticate/login.html', {})
    
def logout_user(request):
    logout(request)
    messages.success(request, ("You were successfully logged out."))
    return redirect("users:login")

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            if request.FILES:
                UserImg.objects.create(user=user, prof_img=request.FILES['prof_img'])
            login(request, user)
            return redirect("todo:listSelect")
        
    else:
        form = SignUpForm()
    
    return render(request, 'authenticate/register_user.html', {'form':form,})