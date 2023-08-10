from django.db import models
from datetime import date, timedelta  # Add this import at the beginning of your models.py

from datetime import date, timedelta  # Add this import at the beginning of your models.py

class FinancialYear(models.Model):
    start_date = models.DateField(default=date.today().replace(month=7, day=1))
    end_date = models.DateField(default=(date.today().replace(month=6, day=30) + timedelta(days=1)))