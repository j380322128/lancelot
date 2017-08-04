# -*- coding: utf-8 -*-
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=20)
    create_time = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='images/category/', null=True)
    
    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
