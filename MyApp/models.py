from django.db import models

from django.contrib.auth.models import User



class Taskmodel(models.Model):
    
    priority_choices=(
        ('1','Low'),
        ('2','Medium'),
        ('3','High'),
    )
    task_name = models.CharField(max_length=100)
    created_date=models.DateField(auto_now_add=True)
    is_completed=models.BooleanField(default=False)
    user_id=models.ForeignKey(User,on_delete=models.CASCADE)
    priority=models.CharField(max_length=10,choices=priority_choices)
    created_date=models.DateField(auto_now_add=True)
    due_date=models.DateField(blank=True)
    completed_date=models.DateField(null=True,blank=True)
    def __str__(self):
        return self.task_name
    
class Points(models.Model):
    points=models.IntegerField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    
    
    def __str__(self):
        return self.points
    
    
   