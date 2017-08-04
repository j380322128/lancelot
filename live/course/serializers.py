# coding: utf-8
from rest_framework import serializers

from django.conf import settings

from anchor.serializers import AnchorSerializer

from .models import CourseInfo
class CourseSerializer(serializers.ModelSerializer):
    anchor = AnchorSerializer()
    class Meta:
        model = CourseInfo
        fields = ('id', 'course_id', 'title', 'description', 'anchor', 'support', 'against', 'start_time', 
                    'end_time', 'status', 'image', 'active', 'audit', 'url')


    