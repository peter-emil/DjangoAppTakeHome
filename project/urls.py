from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import accounts.views
import assets.views

documented_token_refresh_view = swagger_auto_schema(  # pylint: disable=invalid-name
    operation_summary="Refresh Token",
    method="post",
    responses={
        "200": openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "access": openapi.Parameter("access", openapi.IN_BODY, type=openapi.TYPE_STRING)
            }
        )
    }
)(TokenRefreshView.as_view())

urlpatterns = [  # pylint: disable=invalid-name
    path('admin/', admin.site.urls),
    path('accounts/', include([
        path('create/', accounts.views.CreateAccountView.as_view()),
        path('login/', accounts.views.LoginView.as_view()),
        path('tokenrefresh/', documented_token_refresh_view),
    ])),
    path('assets/', include([
        path('metadata/', assets.views.MetadataListCreate.as_view()),
        path('metadata/<name>/', assets.views.MetadataRetrieve.as_view()),
        path('documents/', assets.views.DocumentListCreate.as_view()),
        path('documents/<name>', assets.views.DocumentRetrieve.as_view()),
    ])),
]

schema_view = get_schema_view(  # pylint: disable=invalid-name
    openapi.Info(
        title="Project API",
        default_version='v1.0.0',
        description="Demo Project",
        contact=openapi.Contact(email="pe.peteremil@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [  # pylint: disable=invalid-name
    url(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json'
    ),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + urlpatterns
