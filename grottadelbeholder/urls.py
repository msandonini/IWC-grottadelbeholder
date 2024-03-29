"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.urls import path, include

from ProgettoIWC import settings
from .mylib.views.backup import DataTransferView
from .mylib.views.indexViews import IndexView, InfoView, UserContentView, CreateContentView, \
    ModifyContentView, UserView
from .mylib.views.authViews import LoginView, SigninView, LogoutView

app_name = "grottadelbeholder"
urlpatterns = [
    # Lista contenuti
    path('', IndexView.as_view(), name='index'),
    path('usercontent', UserContentView.as_view(), name='usercontent'),
    # Creazione e modifica contenuti
    path('create', CreateContentView.as_view(), name='create'),
    path('modify', ModifyContentView.as_view(), name='modify'),
    # Gestione utente
    path('login', LoginView.as_view(), name='login'),
    path('signin', SigninView.as_view(), name='signin'),
    path('logout', LogoutView.as_view(), name='logout'),
    # Pagine personali
    path('user', UserView.as_view(), name='user'),
    # Trasferimento dati
    path('datatransfer', DataTransferView.as_view(), name='datatransfer'),
    # Altro
    path('info', InfoView.as_view(), name='info'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
