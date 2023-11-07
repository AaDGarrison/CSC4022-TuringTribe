"""
urls.py

URL patterns for FinApp.
"""

"""
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

# ----------------------------------------------------------------------------
# Django Imports
# ----------------------------------------------------------------------------

from django.contrib import admin
from django.urls import (
    path,
    include,
)

# ----------------------------------------------------------------------------
# Form Imports
# ----------------------------------------------------------------------------

from FinApp.forms import UserLoginForm

# ----------------------------------------------------------------------------
# Imports
# ----------------------------------------------------------------------------

from . import views

# ----------------------------------------------------------------------------
# URL Patterns
# ----------------------------------------------------------------------------

urlpatterns = [

    # Default Django admin page.
    path('admin/', admin.site.urls),

    # Authentication URLS (Login, Logout etc.)
    path('', include('django.contrib.auth.urls')),

    # After Authentication URLs
    path('dashboard/', views.dashboard),
    path('settings/', views.settings),
]
