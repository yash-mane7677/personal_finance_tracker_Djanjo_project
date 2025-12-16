from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta, date  # <--- ADD 'date' HERE

class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    renewal_date = models.DateField()

    @property
    def next_pay_date(self):
        return self.renewal_date + timedelta(days=30)

    @property
    def days_until_renewal(self):
        # This is where 'date' was missing
        delta = self.next_pay_date - date.today() 
        return delta.days

    def __str__(self):
        return self.name