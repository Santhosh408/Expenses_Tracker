from django.db import models
from django.contrib.auth.models import User

class Expenses(models.Model):
    CATEGORY_CHOICES = [
        ('Food','Food'),
        ('Transport','Transport'),
        ('Utilities','Utilities'),
        ('Entertainment','Entertainment'),
        ('Other','Other'),
    ]
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='expenses')
    date = models.DateField()
    amount = models.DecimalField(max_digits=10,decimal_places=2)
    category = models.CharField(max_length=50,choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True,null=True)