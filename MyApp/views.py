from django.shortcuts import render
from django.views.generic import View
from MyApp.forms import UserForm,TaskForm,LoginForm,TaskUpdateForm
from MyApp.models import User,Taskmodel

from django.contrib.auth import authenticate,login




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
            User.objects.create_user(**form.cleaned_data)
            if User.objects.filter(username=form.cleaned_data.get('username')).exists():
                return render(request,'sample.html')
            else:
                return render(request,'registration.html',{'form':form,'error':'User already exists'})
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
                     
                  return render(request,'home.html',{'data':request.user.first_name,'no':request.user.id}) 
              else:
                  return render(request,'login.html',{'form':form,'error':'Invalid username or password'})
                  
                  
          return render(request,'login.html',{'form':form})    
      
class Home(View):
    def get(self,request,**kwargs):
        id=kwargs.get('pk')
        data=User.objects.get(id=id)
        return render(request,'home.html',{'data':data.first_name,'no':data.id})
               
class TaskCreateView(View):
    
    def get(self, request):
        form=TaskForm()
        return render(request,'add_task.html',{'form':form})
    
    def post(self, request):
        form=TaskForm(request.POST)
        
        if form.is_valid():            
            Taskmodel.objects.create(**form.cleaned_data,user_id=request.user)
            print(request.user.id)
            return render(request,"back.html",{'no':request.user.id})  
    
class TaskAll(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        data = Taskmodel.objects.filter(user_id=id)
        return render(request, 'Alltask.html', {'data': data})
            
class TaskDelete(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        Taskmodel.objects.get(id=id).delete()
        return render(request,'back.html',{'no':request.user.id})
    
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
        print(data.user_id.id)
        if form.is_valid():
            form.save()
        
            return render(request,'back.html',{'no':data.user_id.id})
        else:
            return render(request,'Update_task.html',{'form':form}) 
        
                
class Taskdetail(View):
    def get(self, request,**kwargs):
        id=kwargs.get('pk')
        data=Taskmodel.objects.get(id=id)
        return render(request,'Taskdetail.html',{'data':data})
    
    
class Back(View):
    def get(self, request,pk):
        return render(request,'back.html',{'no':pk})
        