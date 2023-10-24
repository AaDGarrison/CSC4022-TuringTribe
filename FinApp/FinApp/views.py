"""
views.py

View methods for FinApp.
"""

# ----------------------------------------------------------------------------
# Django Imports

from django.shortcuts import render
from django.http import HttpResponse

# ----------------------------------------------------------------------------
def login(request):
    return render(request, 'login.html')

# ----------------------------------------------------------------------------
def dashboard(request):
    return render(request, 'dashboard.html')

# ----------------------------------------------------------------------------
def statistics(request):
    return render(request, 'statistics.html')