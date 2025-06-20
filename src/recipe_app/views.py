from django.shortcuts import render, redirect  
#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm    
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def login_view(request):
    login_error = None
    signup_form = SignUpForm()
    
    if request.method == 'POST':
        if 'login' in request.POST:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:recipe_details')
            else:
                login_error = "Invalid username or password."
        elif 'signup' in request.POST:
            signup_form = SignUpForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save(commit=False)
                user.set_password(signup_form.cleaned_data['password'])
                user.save()
                login(request, user)
                return redirect('recipes:recipe_details')

    return render(request, 'login.html', {
        'form': None,  
        'signup_form': signup_form,
        'error_message': login_error
    })

def logout_view(request):                                  
   logout(request)             #pre-defined Django function
   return redirect('login')