from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
import accounts.views

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    path('accounts/', include([
        path('create/', accounts.views.CreateAccountView.as_view()),
        path('login/', accounts.views.LoginView.as_view()),
        path('tokenrefresh/', TokenRefreshView.as_view()),
    ])),
]
