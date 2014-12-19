from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

    
class Account(models.Model):
    owner = models.CharField(max_length=60)
    balance = models.IntegerField() 
    objects = models.Manager()
    
class Operation(models.Model):
    SourceAccount = models.ForeignKey(Account, related_name='SourceAcc')
    TargetAccount = models.ForeignKey(Account, related_name='TargetAcc')
    title = models.TextField()
    amount = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    objects = models.Manager()

    def __unicode__(self):
        return self.title

