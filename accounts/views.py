# pylint:disable=no-self-use
from http import HTTPStatus
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema, no_body
from drf_yasg import openapi


def credentials_in_request_data(data):
    if "email" not in data:
        return views.Response(
            {"error": "email is required"},
            status=HTTPStatus.BAD_REQUEST
        )
    if "password" not in data:
        return views.Response(
            {"error": "password is required"},
            status=HTTPStatus.BAD_REQUEST
        )
    return None


class CreateAccountView(views.APIView):
    @swagger_auto_schema(
        operation_summary="Create New Account",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Parameter('name', openapi.IN_BODY, type=openapi.TYPE_STRING),
                "password": openapi.Parameter('password', openapi.IN_BODY, type=openapi.TYPE_STRING)
            }
        ),
        responses={
            "201": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Parameter(
                        'access',
                        openapi.IN_BODY,
                        type=openapi.TYPE_STRING
                    ),
                    "refresh": openapi.Parameter(
                        'refresh',
                        openapi.IN_BODY,
                        type=openapi.TYPE_STRING
                    )
                }
            ),
            "400": "Bad Request",
            "401": "Unauthorized"
        }
    )
    def post(self, request):
        data = request.data
        err = credentials_in_request_data(data)
        if err is not None:
            return err
        email = data['email']
        password = data['password']
        user, created = User.objects.get_or_create(
            email=email,
            username=email,
        )
        if not created:
            return views.Response(
                {"error": f"User with email {email} already exists"},
                status=HTTPStatus.BAD_REQUEST
            )
        user.set_password(password)
        user.save()
        refresh_token = RefreshToken.for_user(user=user)
        response = {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        }
        return views.Response(
            response,
            status=HTTPStatus.CREATED
        )


class LoginView(views.APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (BasicAuthentication,)

    @swagger_auto_schema(
        operation_summary="Login Endpoint",
        request_body=no_body,
        responses={
            "200": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "access": openapi.Parameter(
                        'access',
                        openapi.IN_BODY,
                        type=openapi.TYPE_STRING
                    ),
                    "refresh": openapi.Parameter(
                        'refresh',
                        openapi.IN_BODY,
                        type=openapi.TYPE_STRING
                    )
                }
            ),
            "401": "Unauthorized"
        }
    )
    def post(self, request):
        user = request.user
        refresh_token = RefreshToken.for_user(user=user)
        response = {
            "access": str(refresh_token.access_token),
            "refresh": str(refresh_token)
        }
        return views.Response(
            response,
            status=HTTPStatus.OK
        )
