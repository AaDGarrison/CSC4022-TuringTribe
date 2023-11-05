"""
views.py

View methods for FinApp.
"""



# ----------------------------------------------------------------------------
# Django Imports
from json import dumps
from django.shortcuts import render
#from FinApp.models import dashboardCardCount
# ----------------------------------------------------------------------------
# View Methods
# ----------------------------------------------------------------------------

# ----------------------------------------------------------------------------
def login(request):
    return render(request, 'registration/login.html')

# ----------------------------------------------------------------------------
def dashboard(request):
    data = {
        "TotalCards":range(5), #dashboardCardCount.objects.get(user=request.user),
        "CardIDJSON": dumps([1222,2333,1444,1555,2666]),
        "CardID": [1222,2333,1444,1555,2666]
    }

    return render(request, 'dashboard.html', {"data": data})

# ----------------------------------------------------------------------------
def statistics(request):
    return render(request, 'statistics.html')

# ----------------------------------------------------------------------------
def settings(request):
    return render(request, 'settings.html')