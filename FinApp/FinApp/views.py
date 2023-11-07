"""
views.py

View methods for FinApp.
"""

# ----------------------------------------------------------------------------
# Django Imports
# ----------------------------------------------------------------------------

from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

from . import forms

# ----------------------------------------------------------------------------
# View Methods/Classes
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
class LoginPageView(View):
    
    template_name = 'registration/login.html'
    form_class = forms.UserLoginForm
    
    #def get(self, request):

        #form = self.form_class()
        #message = ''

        #return render(request, self.template_name, context={'form': form, 'message': message})
        
    def post(self, request):

        form = self.form_class(request.POST)

        if form.is_valid():

            user = authenticate(
                first_name      = form.First_Name,
                last_name       = form.Last_Name,
                email           = form.Email,
                password        = form.Password,
            )

            if user is not None:
                login(request, user)
                return redirect('dashboard/')
            
        message = 'Login failed! Try again.'
        return render(request, self.template_name, context = {'form': form, 'message': message})

# ----------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def dashboard(request):
    data = {
        "TotalCards":range(5), #dashboardCardCount.objects.get(user=request.user),
        "CardID": [222,333,444,555,666]
    }

    return render(request, 'dashboard.html', {"data": data})

# ----------------------------------------------------------------------------
@login_required(login_url='/accounts/login/')
def settings(request):
    return render(request, 'settings.html')