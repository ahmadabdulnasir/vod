#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""

from django.forms import DateTimeInput, DateInput
from django import forms
from django.utils.safestring import mark_safe


class XDSoftDateTimePickerInput(DateTimeInput):
    template_name = "widgets/xdsoft_datetimepicker.html"


class BootstrapDateTimePickerInput(DateTimeInput):
    template_name = "widgets/bootstrap_datetimepicker.html"

    def get_context(self, name, value, attrs):
        datetimepicker_id = "datetimepicker_{name}".format(name=name)
        if attrs is None:
            attrs = dict()
        attrs["data-target"] = "#{id}".format(id=datetimepicker_id)
        attrs["class"] = "form-control datetimepicker-input"
        context = super().get_context(name, value, attrs)
        context["widget"]["datetimepicker_id"] = datetimepicker_id
        return context


class FengyuanChenDatePickerInput(DateInput):
    template_name = "widgets/fengyuanchen_datepicker.html"


# def thumbnail(image_path, width, height):
#     absolute_url = posixpath.join(settings.MEDIA_URL, image_path)
#     return '<img src="%s" alt="%s" class="widget-img" />' % (absolute_url, image_path)


class ImageWidget(forms.widgets.ClearableFileInput):
    template_name = "widgets/image_widget.html"


def boot():
    pass


if __name__ == "__main__":
    boot()
