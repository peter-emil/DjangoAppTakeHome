from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView
import accounts.views
import assets.views

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    path('accounts/', include([
        path('create/', accounts.views.CreateAccountView.as_view()),
        path('login/', accounts.views.LoginView.as_view()),
        path('tokenrefresh/', TokenRefreshView.as_view()),
    ])),
    path('assets/', include([
        path('metadata/', assets.views.MetadataListCreate.as_view()),
        path('metadata/<name>/', assets.views.MetadataRetrieve.as_view()),
        path('documents/', assets.views.DocumentListCreate.as_view()),
        path('documents/<name>', assets.views.DocumentRetrieve.as_view()),
    ])),
]
