"""
URL configuration for everythingvit project.

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
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from authy.views import UserProfile
from django.contrib.auth import views as authViews


urlpatterns = [
    path('',authViews.LoginView.as_view(template_name='login.html'), name='login'),
    path('admin/', admin.site.urls),
    path('post/', include('post.urls')),
    path('user/', include('authy.urls')),
    path('direct/', include('direct.urls')),
    path('<username>/', UserProfile, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

