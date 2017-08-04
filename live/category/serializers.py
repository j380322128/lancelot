from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from .models import Category


class CategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = Category
        fields = ('id', 'name', 'image',
                  'create_time', 
                  )
