from django import forms
from MyApp.models import Taskmodel


class UserForm(forms.Form):
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    first_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    last_name=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    email=forms.EmailField(max_length=100,widget=forms.EmailInput(attrs={'class':'form-control'}))
    
    
class LoginForm(forms.Form):
    
    username=forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control'}))
    password=forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    
    
    
class TaskForm(forms.ModelForm):
    
    class Meta:
        model = Taskmodel
        fields = ('task_name',)
        
        
class TaskUpdateForm(forms.ModelForm):
        
        class Meta:
            model = Taskmodel
            fields = ('task_name','is_completed',)        

    
    
    
    
    
    
    
    
    
    
    
   
    


    
   