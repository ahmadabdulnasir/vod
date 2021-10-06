#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2020, salafi'
__version__ = "0.01t"
"""
from django.http import HttpResponse
from django.conf import settings
import traceback
import logging

logger = logging.getLogger("django_error")


class ErrorHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        error = repr(exception)
        print(error)
        # if not settings.DEBUG:
        # if settings.DEBUG:
        if exception:
            # Format your message here
            message = "**{url}**\n\n{error}\n\n````{tb}````".format(
                url=request.build_absolute_uri(),
                error=repr(exception),
                tb=traceback.format_exc(),
            )
            # print("Error", message)
            # Do now whatever with this message
            # e.g. requests.post(<slack channel/teams channel>, data=message)
            # import logging
            logger.info(f"[ErrorHandlerMiddleware]: {message}")
        return HttpResponse(
            f"Error processing the request. Message: {message}", status=500
        )
