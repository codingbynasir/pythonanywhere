from rest_framework.serializers import ModelSerializer
from medical.models import hospital


class HospitalCreateSerializer(ModelSerializer):
    class Meta:
        model = hospital
        fields = [
            'name',
            'type',
            'email',
            'phone',
            'address',
            'zip_code',
            'division',
        ]

class HospitalListSerializer(ModelSerializer):
    class Meta:
        model = hospital
        fields = [
            'name',
            'type',
            'email',
            'phone',
            'division',
        ]


class HospitalDetailsSerializer(ModelSerializer):
    class Meta:
        model = hospital
        fields = [
            'id',
            'name',
            'type',
            'email',
            'phone',
            'address',
            'zip_code',
            'division',
        ]
