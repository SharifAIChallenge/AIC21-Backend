"""AIC21_Backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView

from apps.accounts.views import GoogleLogin

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/homepage/', include('apps.homepage.urls')),
    path('api/martor/', include('martor.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/subscribe/', include('apps.notification.urls')),
    path('go/', include('apps.go.urls')),
    path('api/go/', include('apps.go.urls')),
    path('api/faq/', include('apps.faq.urls')),
    path('api/staff/', include('apps.staff.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/past/', include('apps.past.urls')),
    path('api/team/', include('apps.team.urls')),
    path('auth/', include('dj_rest_auth.urls')),
    # path('social-login/google/', GoogleLogin.as_view(), name='google_login'),
    path('api/gamedoc/', include('apps.gamedoc.urls')),
    path('api/resources/', include('apps.resources.urls')),
    path('api/ticket/', include('apps.ticket.urls')),
    path('api/courses/', include('apps.course.urls')),
]

# if settings.DEBUG:
urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)
