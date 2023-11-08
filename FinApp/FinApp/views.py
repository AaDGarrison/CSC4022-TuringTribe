"""
views.py

View methods for FinApp.
"""



# ----------------------------------------------------------------------------
# Django Imports
# ----------------------------------------------------------------------------

from json import dumps
from django.contrib.auth.decorators import login_requiredfrom django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

# ----------------------------------------------------------------------------
# View Methods/Classes
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
# Signup
def signupPage(request):

    message = ''
 
    if request.user.is_authenticated:
        return redirect('/dashboard')
     
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
 
        if form.is_valid():

            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('/dashboard')
         
        else:
            message = 'FAILURE TO REGISTER'
            return render(request,'registration/signup.html', {'form': form, 'message': message})
     
    else:

        form = UserCreationForm()
        return render(request,'registration/signup.html', {'form': form, 'message': message})

# ----------------------------------------------------------------------------
# Login
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('/dashboard')

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('/dashboard')
        else:
            form = AuthenticationForm()
            return render(request, 'registration/login.html', {'form': form})
        
    else:

        form = AuthenticationForm()
        return render(request, 'registration/login.html', {'form': form})

# ----------------------------------------------------------------------------
# Logout
@login_required(login_url='')
def logoutPage(request):

    logout(request)
    return redirect('/')

# ----------------------------------------------------------------------------
# Dashboard
@login_required(login_url='')
def dashboard(request):
    data = {
        "TotalCards":range(5), #dashboardCardCount.objects.get(user=request.user),
        "CardIDJSON": dumps([1222,2333,1444,1555,2666]),
        "CardID": [1222,2333,1444,1555,2666]
    }

    return render(request, 'dashboard.html', {"data": data})

# ----------------------------------------------------------------------------
# Settings
@login_required(login_url='')
def settings(request):
    return render(request, 'settings.html')
