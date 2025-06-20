from django.shortcuts import render, redirect  
#Django authentication libraries           
from django.contrib.auth import authenticate, login, logout
#Django Form for authentication
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm 
from django.contrib.auth.models import User
from django.contrib import messages
from django import forms

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

def login_view(request):
    error_message = ''
    form = AuthenticationForm()
    signup_form = UserCreationForm()

    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('recipes:recipe_details')
            else:
                error_message = 'Invalid login credentials.'
        elif 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)  # Automatically log in after signup
                return redirect('recipes:recipe_details')
            else:
                error_message = 'Signup failed. Please check the form.'

    context = {
        'form': form,
        'signup_form': signup_form,
        'error_message': error_message,
    }
    return render(request, 'auth/login.html', context)

def logout_view(request):                                  
   logout(request)             #pre-defined Django function
   return redirect('login')