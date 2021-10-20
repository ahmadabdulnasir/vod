#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""


def get_duration_as_days() -> dict:
    egg = {
        "daily": 1,
        "weekly": 7,
        "monthly": 30,
        "quarterly": 90,
        "yearly": 365,
        "unlimitted": float("inf")
    }
    return egg

def boot():
    pass

if __name__ == "__main__":
    boot()
