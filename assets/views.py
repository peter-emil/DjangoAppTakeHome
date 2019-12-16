from rest_framework import generics, exceptions
from drf_yasg.utils import swagger_auto_schema
from helpers.swagger import get_readable_fields_serializer, get_writable_fields_serializer
from .serializers import MetadataSerializer, DocumentSerializer
from .models import MetadataEntry, DocumentEntry


class MetadataListCreate(generics.ListCreateAPIView):
    serializer_class = MetadataSerializer
    queryset = MetadataEntry.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated
        request.data['owner'] = request.user.pk
        return super().create(request, *args, **kwargs)  # pylint:disable=no-member

    @swagger_auto_schema(
        operation_summary="Create Metadata",
        request_body=get_writable_fields_serializer(MetadataSerializer, exclude=['owner']),
        responses={
            "201": get_readable_fields_serializer(MetadataSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        return super(MetadataListCreate, self).post(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Get All Metadata"
    )
    def get(self, request, *args, **kwargs):
        return super(MetadataListCreate, self).get(request, *args, **kwargs)


class MetadataRetrieve(generics.RetrieveAPIView):
    serializer_class = MetadataSerializer

    def get_object(self):
        return MetadataEntry.objects.get(name=self.kwargs['name'])

    @swagger_auto_schema(
        operation_summary="Get Metadata by name"
    )
    def get(self, request, *args, **kwargs):
        return super(MetadataRetrieve, self).get(request, *args, **kwargs)


class DocumentListCreate(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    queryset = DocumentEntry.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated
        request.data['owner'] = request.user.pk
        return super().create(request, *args, **kwargs)  # pylint:disable=no-member

    @swagger_auto_schema(
        operation_summary="Get Document by name"
    )
    def get(self, request, *args, **kwargs):
        return super(DocumentListCreate, self).get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary="Create Document",
        request_body=get_writable_fields_serializer(DocumentSerializer, exclude=['owner']),
        responses={
            "201": get_readable_fields_serializer(DocumentSerializer)
        }
    )
    def post(self, request, *args, **kwargs):
        return super(DocumentListCreate, self).post(request, *args, **kwargs)


class DocumentRetrieve(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer

    def get_object(self):
        return DocumentEntry.objects.get(name=self.kwargs['name'])

    @swagger_auto_schema(
        operation_summary="Get Document by name"
    )
    def get(self, request, *args, **kwargs):
        return super(DocumentRetrieve, self).get(request, *args, **kwargs)
