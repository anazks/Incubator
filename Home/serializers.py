from rest_framework.serializers import ModelSerializer
from .models import HeartBeatValue

class HBSerializer(ModelSerializer):
    class Meta:
        model = HeartBeatValue
        fields = "__all__"