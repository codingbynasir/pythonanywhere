from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    UpdateAPIView,
    CreateAPIView
)
from medical.models import hospital
from .serializers import (
    HospitalCreateSerializer,
    HospitalListSerializer,
    HospitalDetailsSerializer)


class HospitalCreateApiView(CreateAPIView):
    queryset = hospital.objects.all()
    serializer_class = HospitalCreateSerializer

class HospitalApiView(ListAPIView):
    queryset = hospital.objects.all()
    serializer_class = HospitalListSerializer


class HospitalApiRetrieve(RetrieveAPIView):
    queryset = hospital.objects.all()
    serializer_class = HospitalDetailsSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'


class HospitalApiDelete(DestroyAPIView):
    queryset = hospital.objects.all()
    serializer_class = HospitalListSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'


class HospitalApiUpdate(UpdateAPIView):
    queryset = hospital.objects.all()
    serializer_class = HospitalListSerializer
    lookup_field = 'pk'
    lookup_url_kwarg = 'id'
