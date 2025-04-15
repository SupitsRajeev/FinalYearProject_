from django.db import models

class HREmployee(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    joined_date = models.DateField()

    def __str__(self):
        return f"{self.name} ({self.role})"


class HRSalarySheet(models.Model):
    employee = models.ForeignKey(HREmployee, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # e.g., "April 2025"
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.employee.name} - {self.month}"
