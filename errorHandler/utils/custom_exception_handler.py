#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2020, salafi'
__version__ = "0.01t"
"""

from rest_framework.views import exception_handler


def drf_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)
    # Now add the HTTP status code to the response.
    if response is not None:
        # print(context)
        # print(response.status_code)
        response.data["status_code"] = response.status_code
        # TODO: send mail
    return response
