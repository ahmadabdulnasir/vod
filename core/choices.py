#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = https://ahmadabdulnasir.com.ng
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"
"""
RELIGION_CHOICE = (
    ("islam", "Islam"),
    ("christianity", "Christianity"),
    ("others", "Others"),
)

GENDER_CHOICE = (("male", "Male"), ("female", "Female"), ("others", "Others"))

GUARDIAN_RELATION_WITH_STUDENT_CHOICE = (
    ("parent", "Parent"),
    ("father", "Father"),
    ("mother", "Mother"),
    ("sibling", "Sibling"),
    ("spouse", "Spouse"),
    ("others", "Others"),
)

ENTERY_LEVEL = (("fresh", "Fresh"), ("transfer", "Transfer"))

HEALTH_STATUS = (
    ("Good", "Good"),
    ("Sick", "Sick"),
    ("On Medication", "On Medication"),
    ("Others", "Others"),
)

ETHNICITY_CHOICE = (
    ("fulani", "Fulani"),
    ("hausa", "Hausa"),
    ("hausa-fulani", "Hausa-Fulani"),
    ("igbo", "Igbo"),
    ("yoruba", "Yoruba"),
    # ("tiv", "TIV"),
    # ("ibibio", "Ibibio"),
    # ("nupe", "Nupe"),
)

USER_TYPE_CHOICE = (("free_user", "Free User"), ("premium_user", "Premium User"),
                    ("marchant", "Marchant"), ("staff", "Staff"),
                    ("admin", "Admin"), ("super_admin", "Super Admin"))


CLASS_TYPE = (
    ("education", "Education"),
    ("islamiyya", "Islamiyya"),
    ("Others", "Others"),
)

CLASS_CATEGORY = (
    ("pre_nursery", "Pre Nursery"),
    ("nursery", "Nursery"),
    ("play_group", "Play Group"),
    ("primary", "Primary"),
    ("sss", "Senior Secondary"),
    ("jsss", "Junior Secondary"),
    ("islamiyya", "Islamiyya"),
    ("others", "Others"),
)


TERMS = (
    ("1st Term", "1st Term"),
    ("2nd Term", "2nd Term"),
    ("3rd Term", "3rd Term"),
    ("Others", "Others"),
)

POST_STATUS_CHOICE = (
    ("draft", "Draft"),
    ("review", "Review"),
    ("published", "Publish"),
)

COMMENT_STATUS_CHOICE = (
    ("draft", "Draft"),
    ("review", "Review"),
    ("spam", "Spam"),
    ("approved", "Approved"),
)

DURATION_CHOICE = (
    ("daily", "Daily"),
    ("weekly", "Weekly"),
    ("monthly", "Monthly"),
    ("quarterly", "Quarterly"),
    ("yearly", "Yearly"),
    ("unlimited", "Unlimited"),
)


PLAN_TYPE_CHOICE = (
    ("users", "Users"),
    ("marchants", "Marchants"),
)

ACCESS_LEVEL_CHOICE = (
    ("free", "Free"),
    ("premium", "Premium"),
    ("exclusive", "Exclusive"),
)

def boot():
    pass


if __name__ == "__main__":
    boot()
