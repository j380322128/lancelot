# coding: utf-8
from rest_framework import serializers

from django.conf import settings

from .models import AnchorInfo
class AnchorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AnchorInfo
        fields = ('id', 'user_id', 'name', 'sex', 'tel', 'e_mail', 'title', 'image', 
                    'description', 'reason', 'create_time', 'audit', 'reason')

