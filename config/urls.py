"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt import views as jwtv

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("core/api/", include("core.api.urls"), name="article"),
    path("api/user/", include("account.api.urls"), name="account"),
    path("api/token/access/", jwtv.TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", jwtv.TokenRefreshView.as_view(), name="token_refresh"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# jwt.io check
# for request from terminal:
# curl -H "Authorization: Bearer access_token" url
# curl -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
# .eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjYzNzQ1NDk3LCJpYXQiOjE2NjM3NDUxOTcsImp0aSI6IjM5NjY5YmM2ZTNkMjQzOWVhMjMxYWE3YTc3ZDgyYjNlIiwidXNlcl9pZCI6MX0
# .4sxSU9mTQfodiqab5pl6KXPihrNY6nZkqIIv9gsOLbs" http://127.0.0.1:8000/api/user/me

# for get new access token
# curl -x POST refresh_token_url -d "refresh=refresh_token"
# http://127.0.0.1:8000/api/token/refresh/
