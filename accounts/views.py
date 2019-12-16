from http import HTTPStatus
from rest_framework import views
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken


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
    def post(self, request):  # pylint:disable=no-self-use
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

    def post(self, request):  # pylint:disable=no-self-use
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
