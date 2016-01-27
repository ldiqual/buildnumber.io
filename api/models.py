from __future__ import unicode_literals

import random

from django.db import models
from jsonfield import JSONField

class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class AccountEmail(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name="emails")
    email = models.EmailField(unique=True)

class ApiKey(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name="api_keys")
    key = models.CharField(max_length=40, unique=True) # md5

    def save(self, *args, **kwargs):
        if not self.pk and not self.key:
            hash = random.getrandbits(128)
            self.key = "%032x" % (hash,)
        super(ApiKey, self).save(*args, **kwargs);

class Package(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, related_name="packages")
    name = models.CharField(max_length=255)

class Build(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    package = models.ForeignKey(Package, related_name="builds")
    version = models.CharField(max_length=255, blank=True, null=True)
    build_number = models.PositiveIntegerField()
    extra = JSONField(max_length=1024)

    class Meta:
        unique_together = ('package', 'build_number', 'version')
