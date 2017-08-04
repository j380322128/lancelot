# # -*- coding: utf-8 -*-
# import operator
# from django.shortcuts import render
# from django.views.generic import ListView
# from django import forms
# from django.db.models import Q



# class OwnerList(ListView):
# 	# 关键字查询field, subclass TODO: 子类未重写raise
#     search_fields = None # ["description__contains", "charge_id__contains"]
#     # datetime field TODO: 子类未重写raise
#     datetime_fields = [] # ["createDate"]
#     # default order sort TODO: 子类未重写raise
#     default_order_sort_field = None # ["-createDate"]
#     # models TODO: 子类未重写raise
#     model_class = None
#     form_fields = None # ["channel", "status", "merchant"]
#     # 默认查询，为提供同一个表根据不同的默认条件获取不同意义的数据
#     default_filters = None # {}
#     # 设置request.GET中的key
#     request_key = None # []

#     def get_context_data(self, **kwargs):
#         class OwnerModelForm(forms.ModelForm):
#             class Meta:
#                 model = self.model_class
#                 fields = self.form_fields

#         form_class = OwnerModelForm

#         # 得到子类的类属性值
#         for attr in dir(OwnerList):
#             if getattr(OwnerList, attr) is None and not attr.startswith("__"):
#                 val_attr = getattr(self, attr)
#                 setattr(self, attr, val_attr)

#         context = super(OwnerList, self).get_context_data(**kwargs)
#         if self.form_fields:
#             # 使用form作为筛选条件，搜索结果页默认选中
#             set_dict_val = dict()
#             for field in self.form_fields:
#                 if field in self.request.GET:
#                     search_form_field_val = self.request.GET.get(field)
#                     set_dict_val[field] = search_form_field_val

#             context['form_class'] = form_class
#             if set_dict_val:
#                 context['form_class'] = form_class(data=set_dict_val)

#         # 每个页面使用变量，如果未传入会出现找不到此变量，需要设置默认
#         if self.request_key:
#             request_key_dict = dict.fromkeys(self.request_key, "")
#             context.update(request_key_dict)
#         return context

#         def get_queryset(self):
# 	        # 默认按照创建订单时间倒序
# 	        order_fields = self.request.GET.getlist("order_fields", self.default_order_sort_field)

# 	        # 得到time
# 	        start_time = self.request.GET.get("start_time", None)
# 	        end_time = self.request.GET.get("end_time", None)

# 	        # 排除值为空的key-value, 排除无效属性key-val
# 	        _items = {key: val for key, val in self.request.GET.items() if val and key in dir(self.model_class)}
# 	        _items.pop("order_fields", None)
# 	        # 加入关键字, 使用or关键字
# 	        keywords = self.request.GET.get("keywords", None)
# 	        args = []
# 	        if keywords and self.search_fields:
# 	            search_dict = dict().fromkeys(self.search_fields, keywords)
# 	            q_filter = [Q(**{key: keywords}) for key in self.search_fields if key]
# 	            q_search = reduce(operator.or_, q_filter)
# 	            args.append(q_search)

# 	        # 根据时间筛选
# 	        is_multi_datetime_field = 1 if len(self.datetime_fields) > 1 else 0
	        
# 	        if is_multi_datetime_field:
# 	            pass
# 	        else: # 单个时间字段开始，结束
# 	            if start_time and end_time:
# 	                filter_field_operator = "".join([self.datetime_fields[0], "__", "range"])
# 	                datetime_dict = {filter_field_operator: [start_time, end_time]}
# 	            elif start_time:
# 	                filter_field_operator = "".join([self.datetime_fields[0], "__", "gte"])
# 	                datetime_dict = {filter_field_operator: start_time}
# 	            elif end_time:
# 	                filter_field_operator = "".join([self.datetime_fields[0], "__", "lte"])
# 	                datetime_dict = {filter_field_operator: end_time}
# 	            else:
# 	                datetime_dict = {}
# 	            args.append(Q(**datetime_dict))

# 	        filter_fields = _items
# 	        # 默认查询，为提供同一个表根据不同的默认条件获取不同意义的数据
# 	        if self.default_filters:    
# 	            filter_fields.update(self.default_filters)

# 	        object_list = self.model_class.objects.filter(*args, **filter_fields).order_by(*order_fields)
# 	        return object_list

