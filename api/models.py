from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.utils import timezone

class GetRequest(models.Model):

    code = models.CharField(
        max_length=200, blank=True, null=True)
    user = models.ForeignKey(
        User, null=True, blank=True, on_delete=models.SET_NULL)
    nin = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(max_length=200, blank=True, null=True)
    date_req = models.DateTimeField(blank=True, null=True, default=timezone.now)
    update_in = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        ref = '-'

        if self.nin:
            ref = str(self.nin).lower()

        return ref
  
