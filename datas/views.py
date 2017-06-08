# -*- coding: utf-8 -*-
"""
Datas REST Framework

https://iothook.com/
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponseRedirect
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse

from rest_framework import routers, serializers, viewsets
from rest_framework import views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import permissions

from chartit import DataPool, Chart

from channels.forms import ChannelForm
from channels.models import Channel
from datas.models import Data
from datas.permissions import IsOwnerOrReadOnly
from datas.serializers import DataSerializer
from iotdashboard.debug import debug


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class Datas(views.APIView):
    """
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        datas = Data.objects.all()
        serializer = DataSerializer(datas, many=True)
        return Response(serializer.data)


    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        data = JSONParser().parse(request)

        data['owner'] = self.request.user.pk

        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            data['remote_address'] = x_forwarded_for.split(',')[-1].strip()
        else:
            data['remote_address'] = request.META.get('REMOTE_ADDR') + "&" + request.META.get('HTTP_USER_AGENT') + "&" + request.META.get('SERVER_PROTOCOL')

        data['channel'] = get_object_or_404(Channel, api_key=data['api_key']).pk

        debug(data)

        serializer = DataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DataDetail(views.APIView):
    """
    Retrieve, update or delete a datas instance.
    """
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


    def get_object(self, pk):
        """
        :param request:
        :param pk:
        :return:
        """
        try:
            return Data.objects.get(pk=pk)
        except Data.DoesNotExist:
            raise Http404


    def get(self, request, pk, format=None):
        """
        :param request:
        :param pk:
        :param format:
        :return:
        """
        datas = self.get_object(pk)
        serializer = DataSerializer(datas)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        """
        :param request:
        :param pk:
        :param format:
        :return:
        """
        datas = self.get_object(pk)
        serializer = DataSerializer(datas, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        """
        :param request:
        :param pk:
        :param format:
        :return:
        """
        datas = self.get_object(pk)
        datas.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class DataQueryList(TemplateView):
    """
    All data list for template.
    """
    template_name = "back/data_list.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        datas = Data.objects.all().order_by('-pub_date')[:100]

        element_id_1 = False
        element_id_2 = False
        element_id_3 = False
        element_id_4 = False
        element_id_5 = False
        element_id_6 = False
        element_id_7 = False
        element_id_8 = False
        element_id_9 = False
        element_id_10 = False

        for i in datas:
            if i.element_id_1:
                element_id_1 = True
            if i.element_id_2:
                element_id_2 = True
            if i.element_id_3:
                element_id_3 = True
            if i.element_id_4:
                element_id_4 = True
            if i.element_id_5:
                element_id_5 = True
            if i.element_id_6:
                element_id_6 = True
            if i.element_id_7:
                element_id_7 = True
            if i.element_id_8:
                element_id_8 = True
            if i.element_id_9:
                element_id_9 = True
            if i.element_id_10:
                element_id_10 = True

        return render(request, self.template_name, {'datas': datas,
                                                    'element_id_1':element_id_1,
                                                    'element_id_2':element_id_2,
                                                    'element_id_3':element_id_3,
                                                    'element_id_4':element_id_4,
                                                    'element_id_5':element_id_5,
                                                    'element_id_6':element_id_6,
                                                    'element_id_7':element_id_7,
                                                    'element_id_8':element_id_8,
                                                    'element_id_9':element_id_9,
                                                    'element_id_10':element_id_10
                                                    })
