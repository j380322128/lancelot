# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView, ListView, View, DetailView, CreateView

from .models import Category
from django.conf import settings

# Create your views here.
@method_decorator(login_required, name='dispatch')
class CategoryList(ListView):
    """
    广告列表
    """
    template_name = 'category/category.html'
    context_object_name = 'obj_list'

    def get_queryset(self):
        category_list = Category.objects.all()
        return category_list

    def get_context_data(self, **kwargs):
        context = super(CategoryList, self).get_context_data(**kwargs)
        category_id = self.request.GET.get('category_id', '')
        category_info = None
        if category_id:
            category_info = Category.objects.filter(pk=category_id).first()
        context['category_info'] = category_info
        return context


@login_required()
def upload_picture(request):
    if request.method == "POST":
        category_id = request.POST.get('category_id', '')
        name = request.POST.get('category_name', '')
        image = request.FILES.get('image', None)
 
        if category_id:
            category = Category.objects.get(pk=category_id)
            if name:
                category.name = name
            if image:
                category.image = image
        else:
            category = Category(image=image, name=name)
        category.save()
        return redirect('category:category_list', )
    else:
        return JsonResponse({'result': 'fail', 'message': u'请求错误,请联系管理员！'})
