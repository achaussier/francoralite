from rest_framework import viewsets
from ..models.mediatype import MediaType as MediaTypeModel
from ..serializers.mediatype import MediaTypeSerializer


class MediaTypeViewSet(viewsets.ModelViewSet):
    """
    MediaType management
    """

    queryset = MediaTypeModel.objects.all()
    serializer_class = MediaTypeSerializer
