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
    if request.method == 'POST':
        if 'login' in request.POST:
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                user = form.get_user()
                login(request, user)
                return redirect('home')  # or wherever your home page is
            else:
                error_message = 'Invalid login'
        elif 'signup' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                signup_form.save()
                return redirect('login')  # go back to login after signup
            else:
                error_message = 'Signup failed'
    else:
        form = AuthenticationForm()
        signup_form = UserCreationForm()

    return render(request, 'login.html', {
        'form': form,
        'signup_form': signup_form,
        'error_message': error_message,
    })

def logout_view(request):                                  
   logout(request)             #pre-defined Django function
   return redirect('login')