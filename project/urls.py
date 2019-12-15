from django.contrib import admin
from django.urls import path

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
]
