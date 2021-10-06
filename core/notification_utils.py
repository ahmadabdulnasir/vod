#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Ahmad Abdulnasir Shuaib <me@ahmadabdulnasir.com.ng>'
__homepage__ = 'https://ahmadabdulnasir.com.ng'
__copyright__ = 'Copyright (c) 2021, salafi'
__version__ = "0.01t"



from django.core.mail import send_mail
from django.conf import settings


# from_email = settings.SERVER_EMAIL
from_email = settings.EMAIL_HOST_USER

signature = """
            ---------------------------------------
            This is an auto-generated email, do not reply to this mail.
            NB: 
            The information transmitted is intended only for the person or entity to which it is addressed 
            and may contain confidential and or privileged material. Any review, retransmission, 
            dissemination or other use or any action taken in reliance upon this information by persons or 
            entities other than the intended recipient is prohibited. If you receive this mail in error, 
            please contact the sender and delete the material from your Computer system.
            """

signature = """
            ---------------------------------------
            This is an auto-generated email, do not reply to this mail.
            """


def customMailing(subject, to_emails, msg):
    try:
        send_mail(
            subject=subject,
            message=msg,
            # html_message=html_message
            from_email=from_email,
            recipient_list=to_emails,
            fail_silently=False,
        )
        # print("MEssage Sent")
    except Exception as exp:
        print(exp)
        pass


def contactCreationMail(contact_us):
    subject = "BIG Trust Academy | New Contact Us Message"
    msg = f"""
            Dear Admin,
            Someone Fill Contact Us Page. See detail below:
            Name: {contact_us.name}
            Email: {contact_us.email}
            Pubject: {contact_us.subject}
            Phone: {contact_us.phone}
            Message: {contact_us.message}
            Date Submitted: {contact_us.date_submitted}

            {signature}
        """
    to_emails = ["info@bigtrustacademy.com"]
    customMailing(subject, to_emails, msg)


def surveyApprovalMail(user, survey):
    subject = "GFSO | Survey Approved"
    msg = f"""
            Dear {user.username},
            This is to notify you of an Approval to the Survey you Created detail below:
            Survey: {survey.title}
            Quarter: {survey.quarter}
            Year: {survey.year}
            Survey Type: {survey.survey_type}
            Approved By: {survey.approved_by}
            Approved on: {survey.approved_timestamp}
            Start Date: {survey.start_date}
            Due Date: {survey.due_date}
            Created on: {survey.created}

            {signature}
        """
    to_emails = [user.email]
    customMailing(subject, to_emails, msg, user, survey)


def surveyRejectionlMail(user, survey):
    subject = "GFSO | Survey Rejected"
    msg = f"""
            Dear {user.username},
            This is to notify you that the Survey you Created  has been Rejected, see detail below:
            Survey: {survey.title}
            Quarter: {survey.quarter}
            Year: {survey.year}
            Survey Type: {survey.survey_type}
            Rejected on: {survey.updated}
            Remark: {survey.rejection_remark}
            Start Date: {survey.start_date}
            Due Date: {survey.due_date}
            Created on: {survey.created}

            {signature}
        """
    to_emails = [user.email]
    customMailing(subject, to_emails, msg, user, survey)


def surveyDeletionMail(user, survey):
    subject = "GFSO | Survey Deleted"
    msg = f"""
            Dear {user.username},
            You have Successfully Created a Survey detail below:
            Survey: {survey.title}
            Quarter: {survey.quarter}
            Year: {survey.year}
            Survey Type: {survey.survey_type}
            Start Date: {survey.start_date}
            Due Date: {survey.due_date}
            Created on: {survey.created}

            {signature}
        """
    to_emails = [user.email]
    customMailing(subject, to_emails, msg, user, survey)
