# -*- coding: utf-8 -*-

from django.forms import ModelForm

from .models import *


class ChannelForm(ModelForm):
    required_css_class = 'required'
    class Meta:
        model = Channel
        fields = [
            'channel_name',
            'description',
            'element_1',
            'element_2',
            'element_3',
            'element_4',
            'element_5',
            'element_6',
            'element_7',
            'element_8',
            'element_9',
            'element_10',
            'enable',
        ]

    def __init__(self, *args, **kwargs):
        super(ChannelForm, self).__init__(*args, **kwargs)
        for i in self.fields:
            if i not in ['enable']:
                self.fields[i].widget.attrs['class'] = 'form-control'
