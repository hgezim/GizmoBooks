from django.db import models

def user_from_email(email):
    # TODO: figure out a way to deal with existing emails
    # create user based on email; ensure email doesn't already exist
    # TODO: in fact make email a unique field?! not sure if contrib.auth will allow this
    # if email exists:
    #    figure out a way to post it anyway and maybe send a different email to user with
    #    password reminder
    # 
