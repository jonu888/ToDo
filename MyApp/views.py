from django.shortcuts import render,redirect
from django.views.generic import View
from MyApp.forms import UserForm,TaskForm,LoginForm,TaskUpdateForm
from MyApp.models import User,Taskmodel,Points

from django.contrib.auth import authenticate,login,logout
from datetime import datetime, date
from django.utils.decorators import method_decorator
from django.views import View
from django.shortcuts import render
from datetime import datetime, timedelta
from .models import Taskmodel, Points  # Assuming Taskmodel and Points are your models
from django.contrib.auth.models import User


def is_user(fn):
    
    def wrapper(request,**kwargs):
    
        id=kwargs.get('pk')
        obj=Taskmodel.objects.get(id=id)
        if obj.user_id==request.user:
            return fn(request,**kwargs)
        else:
            return redirect("login")
        
    return wrapper

 
class Welcome(View):
    def get(self,request):
        return render(request,'welcome.html')
    
class Registration(View):
    
    def get(self, request):
        
        form=UserForm()
        return render(request, 'registration.html',{'form':form})
    
    
    def post(self, request):
        
        form=UserForm(request.POST)
        
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return render(request,'registration.html',{'form':form,'error':'User already exists'})
            else:
                User.objects.create_user(**form.cleaned_data)
                data=LoginForm()
                return render(request,'sample.html')
        form=UserForm()    
        return render(request,'registration.html',{'form':form})
    
class Login(View):
    
      def get(self, request):
          form=LoginForm()
          return render(request,'login.html',{'form':form})
      
      def post(self,request):
          form=LoginForm(request.POST)
          
          if form.is_valid():

              name=form.cleaned_data.get('username')
              pswd=form.cleaned_data.get('password')
              
              user=authenticate(request,username=name,password=pswd)
              
              if user:
                  login(request,user) 
                  taskdata = Taskmodel.objects.filter(user_id=request.user)
                  completed_tasks = taskdata.filter(is_completed=1).count()
                  pending_tasks = taskdata.filter(is_completed=0).count()
                  return render(request,'home.html',{'data':request.user.first_name,'no':request.user.id,'task':taskdata,'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks}) 
              else:
                  return render(request,'login.html',{'form':form,'error':'Invalid username or password'})
                  
                  
          return render(request,'login.html',{'form':form})    
      
class Home(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        data=User.objects.get(id=id)
        taskdata = Taskmodel.objects.filter(user_id=request.user)
        completed_tasks = taskdata.filter(is_completed=1).count()
        pending_tasks = taskdata.filter(is_completed=0).count()
        return render(request,'home.html',{'data':data.first_name,'no':data.id,'task':taskdata,'completed_tasks': completed_tasks,
        'pending_tasks': pending_tasks})
               
class TaskCreateView(View):
    
    def get(self, request):
        form=TaskForm()
        return render(request,'add_task.html',{'form':form})
    
    def post(self, request):
        form=TaskForm(request.POST)
        
        if form.is_valid():            
            Taskmodel.objects.create(**form.cleaned_data,user_id=request.user)
            return redirect('taskall',pk=request.user.id)
        else:
            return render(request,'add_task.html',{'form':form})
    
    
    
    
def calculate_remaining_days(due_date):
    if due_date:
        today = date.today()
        
        remaining_days = (due_date - today).days
        return remaining_days
    return None



class TaskAll(View):
    def get(self, request, **kwargs):
        id = kwargs.get('pk')
        
        # Non-expired pending tasks (ordered by priority high to low)
        non_expired_tasks = Taskmodel.objects.filter(
            user_id=id,
            is_completed=False,
            due_date__gte=datetime.now()  # Non-expired tasks
        ).order_by('-priority')  # High priority (3) to low (1)
        
        # Completed tasks (ordered by completion date, most recent first)
        completed_tasks = Taskmodel.objects.filter(
            user_id=id,
            is_completed=True
        ).order_by('-completed_date')
        
        
        

        # Expired tasks (ordered by due date, most recent first)
        expired_tasks = Taskmodel.objects.filter(
            user_id=id,
            is_completed=False,
            due_date__lt=datetime.now()
        ).order_by('-due_date')

        

        # Combine the querysets in the desired order
        tasks = list(non_expired_tasks) + list(completed_tasks) + list(expired_tasks)

        # Calculate remaining days and status for each task
        for task in tasks:
            if not task.is_completed and task.due_date:
                task.remaining_days = calculate_remaining_days(task.due_date)
                if task.remaining_days is not None:
                    if task.remaining_days < 0:
                        task.status_color = 'text-danger'  # Overdue/Expired
                        task.overdue_days = abs(task.remaining_days)
                    elif task.remaining_days <= 2:
                        task.status_color = 'text-warning'  # Due soon
                    else:
                        task.status_color = 'text-dark'  # Plenty of time

        # Get total points
        try:
            total_points = Points.objects.get(user_id=request.user.id)
            points = total_points.points
        except Points.DoesNotExist:
            points = 0  # Default to 0 if no points record exists

        return render(request, 'Alltask.html', {'no': request.user.id, 'data': tasks, 'points': points})


@method_decorator(decorator=is_user,name='dispatch')            
class TaskDelete(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        Taskmodel.objects.get(id=id).delete()
        data = Taskmodel.objects.filter(user_id=request.user.id).order_by('is_completed','-priority')
        return redirect('taskall',pk=request.user.id)
    
    
    
@method_decorator(decorator=is_user,name='dispatch')     
class TaskUpdate(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        data=Taskmodel.objects.get(id=id)
        form=TaskUpdateForm(instance=data)
        return render(request,'Update_task.html',{'form':form,'id':id})
    
    def post(self, request,**kwargs):
        id=kwargs.get('pk')
        data=Taskmodel.objects.get(id=id)
        form=TaskUpdateForm(request.POST,instance=data)
        if form.is_valid():
            form.save()
            return redirect('taskall',pk=request.user.id)
        else:
            return render(request,'Update_task.html',{'form':form}) 
        
@method_decorator(decorator=is_user,name='dispatch')                 
class Taskdetail(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        data=Taskmodel.objects.get(id=id)
        return render(request,'Taskdetail.html',{'data':data})
    
@method_decorator(decorator=is_user,name='dispatch')      
class completedtask(View):
    def get(self, request, **kwargs):
        id = kwargs.get('pk')
        task = Taskmodel.objects.get(id=id)
        task.is_completed = True
        task.completed_date = datetime.now()
        
        # Calculate points based on completion time
        if task.due_date:
            # Convert dates to datetime for proper calculation
            due_date = datetime.combine(task.due_date, datetime.min.time())
            created_date = datetime.combine(task.created_date, datetime.min.time())
            completed_date = task.completed_date
            
            # Calculate time differences
            total_duration = (due_date - created_date).total_seconds()
            time_taken = (completed_date - created_date).total_seconds()
            
            # Calculate completion percentage
            if total_duration > 0:
                completion_percentage = (time_taken / total_duration) * 100
                
                # Assign points based on completion time
                if completion_percentage <= 25:
                    points_to_add = 10  # Completed within first 25% of time
                elif completion_percentage <= 50:
                    points_to_add = 8   # Completed within first 50% of time
                elif completion_percentage <= 75:
                    points_to_add = 5   # Completed within first 75% of time
                else:
                    points_to_add = 3   # Completed in the last 25% of time
            else:
                points_to_add = 1  # Default points if due date is same as created date
        else:
            points_to_add = 1  # Default points if no due date is set
        
        # Update user points
        user = User.objects.get(id=task.user_id.id)
        points, created = Points.objects.get_or_create(user=user)
        points.points += points_to_add
        points.save()
            
        task.save()
        
        return redirect('taskall',pk=request.user.id)
  
class Profile(View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        tasks = Taskmodel.objects.filter(user_id=user)
        
        # Calculate statistics
        total_tasks = tasks.count()
        completed_tasks = tasks.filter(is_completed=True).count()
        
        # Get user points
        points, _ = Points.objects.get_or_create(user=user)
        
        context = {
            'user': user,
            'no': pk,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'points': points.points
        }
        
        return render(request, 'profile.html', context)  
    

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    
    
    
    
    
    
  