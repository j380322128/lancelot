# -*- coding: utf-8 -*-

from collections import OrderedDict

from rest_framework import viewsets
from rest_framework import filters
from rest_framework.decorators import detail_route
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status

from .serializers import CategorySerializer
from .models import Category
from course.models import CourseInfo
from course.serializers import CourseSerializer




class CategoryViewSet(viewsets.ModelViewSet):
    # """
    # 这一viewset提供了`list`, `create`, `retrieve`, `update` 和 `destroy`
    # """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = (filters.DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)

    filter_fields = ('name',)
   

    def destroy(self, request, pk):
        '''
        删除广告
        :param validated_data:
        :return:
        '''
        # 当前登录用户
        course = CourseInfo.objects.filter(category_id=pk)
        if course:
            raise ServiceConflict(detail='该分类下存在课程')
        else:
            category = Category.objects.get(pk=pk)
            category.delete()
        return Response('删除成功', status=status.HTTP_200_OK)

    @detail_route()
    def courses(self, request, pk):
        sort = request.GET.get('sort', '')
        filter = request.GET.get('filter', '')
   
        if pk != 'all':
            course_info = CourseInfo.objects.filter(category_id=pk, active=1)
        else:
            course_info = CourseInfo.objects.filter(active=1)

        if 'free' in filter:
            course_info = course_info.filter(money=0)

        if 'update_at' in sort:
            course_list = course_info.order_by('-start_time')
        else:
            course_list = course_info.order_by('-create_time')
        if 'sales' in sort :
            course_info = []
            for i in course_list:
                count = MyCourse.objects.filter(course_id=i.course_id).count()
                course_info.append({'course_id':i.course_id, 'count':count})

            course_info.sort(key=lambda k: (k.get('count', 0)),reverse=True)
            course_list = []
            for c in course_info:
                course = CourseInfo.objects.get(course_id=c['course_id'])
                course_list.append(course)

        if 'selection' in sort:
            course_list = course_info.filter(select_status=SELECT_STATUS_ON)

        page = self.paginate_queryset(course_list)
        serializer = CourseSerializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @detail_route(methods=['delete'])
    def delete_category(self, request, pk):
        course = CourseInfo.objects.filter(category_id=pk)
        if course:
            for i in course:
                i.category_id = None
                i.save()
        category = Category.objects.get(pk=pk)
        category.delete()
        return Response('删除成功', status=status.HTTP_200_OK)