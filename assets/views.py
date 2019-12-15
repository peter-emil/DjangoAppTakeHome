from rest_framework import generics, exceptions
from .serializers import MetadataSerializer
from .models import MetadataEntry


class MetadataListCreate(generics.ListCreateAPIView):
    serializer_class = MetadataSerializer
    queryset = MetadataEntry.objects.all()

    def create(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            raise exceptions.NotAuthenticated
        return super().create(request, *args, **kwargs)


class MetadataRetrieve(generics.RetrieveAPIView):
    serializer_class = MetadataSerializer

    def get_object(self):
        return MetadataEntry.objects.get(name=self.kwargs['name'])
