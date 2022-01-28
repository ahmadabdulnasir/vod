#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = 'https://ahmadabdulnasir.com.ng'
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"

from .serializers import CustomeSerializer

from core.models import MainPage, SiteInformation


class MainPageDetailsSerializer(CustomeSerializer):

    class Meta:
        model = MainPage
        fields = [
            "pk",
            "title",
            "slug",
            "sub_title",
            "body",
            "youtube_video_id",
            "extra_info",
            "on_navigation",
            "timestamp",
            "updated",
        ]


class MainPageListSerializer(CustomeSerializer):

    class Meta:
        model = MainPage
        fields = [
            "pk",
            "title",
            "slug",
            "sub_title",
            # "body",
            # "youtube_video_id",
            # "extra_info",
            "on_navigation",
            "timestamp",
            "updated",
        ]


class SiteInformationDetailsSerializer(CustomeSerializer):

    class Meta:
        model = SiteInformation
        fields = [
            "pk",
            "title",
            "slug",
            "info",
            "active",
            "timestamp",
            "updated",
        ]


class SiteInformationListSerializer(CustomeSerializer):

    class Meta:
        model = SiteInformation
        fields = [
            "pk",
            "title",
            "slug",
            "active",
            "timestamp",
            "updated",
        ]
