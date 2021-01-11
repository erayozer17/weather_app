from django.db import models
from django.utils.translation import ugettext_lazy as _

class City(models.Model):
    name = models.CharField(_("City Name"), max_length=50)