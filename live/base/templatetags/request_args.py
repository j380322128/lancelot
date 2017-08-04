# coding: utf-8
from django import template

register = template.Library()


@register.filter(name="ck_request_args")
def check_request_args(request, args):
    val = request.get(args, "")
    return val