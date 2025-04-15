from django.db import models

class HREmployee(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.name} - {self.department}"