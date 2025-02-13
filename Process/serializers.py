from rest_framework import serializers
from .models import EndPoint


class EndPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = EndPoint
        fields = ['id','user_name','user_id','resume','prompt','time']
