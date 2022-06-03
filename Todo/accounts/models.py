from pyexpat import model
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

def get_name(self):
    name = ''
    if self.first_name: 
        name += self.first_name.strip()
    if self.last_name:
        name += self.last_name.strip()
    if name:
        return name
    return self.username

User.add_to_class('get_name', get_name)

