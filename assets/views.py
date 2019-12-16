from rest_framework import generics, exceptions
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


class MetadataRetrieve(generics.RetrieveAPIView):
    serializer_class = MetadataSerializer

    def get_object(self):
        return MetadataEntry.objects.get(name=self.kwargs['name'])


class DocumentListCreate(generics.ListCreateAPIView):
    serializer_class = DocumentSerializer
    queryset = DocumentEntry.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated
        request.data['owner'] = request.user.pk
        return super().create(request, *args, **kwargs)  # pylint:disable=no-member


class DocumentRetrieve(generics.RetrieveAPIView):
    serializer_class = DocumentSerializer

    def get_object(self):
        return DocumentEntry.objects.get(name=self.kwargs['name'])
