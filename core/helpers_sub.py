#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shu'aib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2019, salafi'
__version__ = "0.01t"
"""
from uuid import uuid4
from core.models import SiteInformation, Partner
from gallery.models import Image


# def siteLoginUrl():
#     return 'accounts/login/'

# def themeVersion():
#     ''' return the current active theme/template '''
#     try:
#         theme = SiteInformation.objects.filter(slug__contains='default-theme').order_by('-updated').first()
#         theme = theme.info
#     except Exception as e:
#         theme = 'v3/'
#     finally:
#         # print(theme)
#         if theme.endswith('/'):
#             return theme
#         else:
#             return theme+'/'


def getSitePhone(num=0):
    try:
        phones = SiteInformation.objects.filter(slug__contains="phone")
        if num > 0:
            return phones[:num]
        else:
            return phones[num]
    except Exception as e:
        return "+2348035971242"


def getSiteEmail():
    try:
        email = (
            SiteInformation.objects.filter(slug__contains="email")
            .order_by("-updated")
            .first()
        )
        if not email:
            mail = "me@ahmadabdulnasir.com.ng"
        else:
            mail = email.info
    except Exception as e:
        mail = "me@ahmadabdulnasir.com.ng"
    finally:
        return mail


def getSiteAddress():
    try:
        address = (
            SiteInformation.objects.filter(slug__contains="address")
            .order_by("-updated")
            .first()
        )
        if not address:
            address = "me@ahmadabdulnasir.com.ng"
        else:
            address = address.info
    except Exception as e:
        address = "me@ahmadabdulnasir.com.ng"
    finally:
        return address


def getSiteSocial(social="twitter"):
    try:
        site = (
            SiteInformation.objects.filter(slug__contains=social)
            .order_by("-updated")
            .first()
        )
        if not site:
            if social == "staff_mail":
                site = "https://mail.zoho.com/zm/"
            else:
                site = "https://ahmadabdulnasir.com.ng"
        else:
            site = site.info
    except Exception as exp:
        if social == "staff_mail":
            site = "https://mail.zoho.com/zm/"
        else:
            site = "https://ahmadabdulnasir.com.ng"
    finally:
        return site


def getSiteTagline():
    try:
        info = (
            SiteInformation.objects.filter(slug__contains="tagline")
            .order_by("-updated")
            .first()
        )
        if not info:
            info = "DaboLinux Technologies - The Feture in Your Hands"
        else:
            info = info.info
    except Exception as e:
        info = "DaboLinux Technologies - The Feture in Your Hands"
    finally:
        return info


def getAnalyticsId():
    try:
        info = (
            SiteInformation.objects.filter(slug__contains="analytics")
            .order_by("-updated")
            .first()
        )
        if not info:
            info = ""
        else:
            info = info.info
    except Exception as e:
        info = ""
    finally:
        return info


def getSiteMedia(num=0):
    try:
        media = Image.objects.all()
        if num != 0:
            print(len(media))
            return media[:num]
        else:
            print(len(media))
            return media[num]
    except Exception as e:
        return []


def getSitePartners():
    try:
        partners = Partner.objects.all().order_by("-updated")
        return partners
    except Exception as e:
        return []


PAYMENT_GATEWAY_KEYS = {
    "paystack-public-key": "pk_test_56fb985ccde08b20dec70ea03feac02ccdb01036",
    "paystack-secret-key": "pk_test_56fb985ccde08b20dec70ea03feac02ccdb01036",
    "paystack-sub-account-id": "ACCT_sk1jwvj306i0xgc",
    "flutterwave-public-key": "FLWPUBK_TEST-66a316473b102e02094930b48e9673ba-X",
    "flutterwave-secret-key": "FLWSECK_TEST-86c7e7b7c26b02a6d7fcd620b4a0f99c-X",
    "flutterwave-sub-account-id": "RS_180EFB5415DAC7FDE74C730D53A2B7EB",
}

def getPaymentKey(value):
    # value = value+' payment'
    try:
        info = SiteInformation.objects.get(slug=value)
        if not info:
            print("[DEBUG]: Payment Key Not Found, Using Test Key")
            info = f"{PAYMENT_GATEWAY_KEYS.get(value)}"
        else:
            info = info.info
            print("[DEBUG]: Payment Key Found", info)
    except Exception as exp:
        print("[DEBUG]: Payment Key Not Found Exception, Using Test Key")
        info = f"{PAYMENT_GATEWAY_KEYS.get(value)}"
        print(exp)
    finally:
        return info


def getSiteLongitude():
    try:
        info = (
            SiteInformation.objects.filter(slug__contains="longitude")
            .order_by("-updated")
            .first()
        )
        if not info:
            info = "11.9816113"
        else:
            info = info.info
    except Exception as e:
        info = "11.9816113"
    finally:
        return info


def getSiteLatitude():
    try:
        info = (
            SiteInformation.objects.filter(slug__contains="latitude")
            .order_by("-updated")
            .first()
        )
        if not info:
            info = "8.4684441"
        else:
            info = info.info
    except Exception as e:
        info = "8.4684441"
    finally:
        return info


class DaboLinux:
    def __init__(self):
        self.name = "DaboLinux Technologies CMS Solution"
        self.description = "DaboLinux Technologies Content Management Software Solution"
        self.sale_email = "sales@dabolinux.com"
        self.contact_email = "info@dabolinux.com"  #'contact@dabolinux.com'
        self.phones = ["+2348035971242", "+2348182788350"]
        self.title = "DaboLinux CMS"
        self.website = "https://www.dabolinux.com"
        self.short = "Dabolinux Technologies"
        self.short_software_name = "DL SMS"
        _, q = self.info(), self.developer()

    def developer(self):
        self.dev_name = "Ahmad Abdulnasir Shuaib"
        self.dev_p_email = "me@ahmadabdulnasir.com.ng"
        self.dev_email = "ahmad@dabolinux.com"
        self.dev_phone = "+2348035971242"
        self.dev_website = "https://ahmadabdulnasir.com.ng/me/"
        return self.dev_name

    def info(self):
        self.text = f"""
        <p>{self.name} started in 2018 with a single bit of code to enhance the record management
         in primary and secondary schools in Nigeria. Since then it has grown with more 
         features that involve financial managment and tracking as well as easy data accessibility
         by users. The primary goal of building this software is to simplify the traditional methods
         of storing, managing and processing data in all Academia.</p>
        <p>Everything you see here, from the documentation to the code itself,
        was created by the team of <a href="{self.website}" target="_blank">{self.short}</a>. who still maintain the softawre. 
        All issues and bugs concerning this software are to be submitted to 
        <a href="{self.website}" target="_blank">{self.short}</a>.</p>
        <p>This software is Property of {self.short}</p>
        <p>This Software may be sold or marketted by a third party partner,
        but  will still maintain the licence of <a href="{self.website}" target="_blank">{self.short}</a></p>

        <p>For more Information, reach us on {self.contact_email}</p>
        """
        self.version = "Version 0.2 Beta"
        self.last_update = "04<sup>th</sup> July, 2020</p>"

    def __str__(self):
        return self.name
