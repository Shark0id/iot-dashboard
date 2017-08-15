# -*- coding: utf-8 -*-
"""
Iotdashboard project
Django 1.10.1
Python 2.7.6

Author: Sahin MERSIN

Demo: http://iotdashboard.pythonanywhere.com
Source: https://github.com/electrocoder/iotdashboard

https://iothook.com/
http://mesebilisim.com

Licensed under the Apache License, Version 2.0 (the "License").
You may not use this file except in compliance with the License.
A copy of the License is located at

http://www.apache.org/licenses/
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


class Datas(views.APIView):
    """
    """
    def get(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        try:
            if request.GET['data'] == 'first':
                datas = Data.objects.order_by('pub_date')[:1]
            elif request.GET['data'] == 'last':
                datas = Data.objects.order_by('-pub_date')[:1]
        except:
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


        data['owner'] = 1

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

