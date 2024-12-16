from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .form import LoginForm, UserRegistrationForm,\
UserEditForm,ProfileEditorForm
from django.contrib import messages
from .models import Profile

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard(request):
    return render(request,'account/dashboard.html',{'section':'dashboard'})





def register(request):
   
    if request.method  == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #create a new user object 
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()

            #create the user profile
            Profile.objects.create(user=new_user)
            return render(request,'account/register_done.html',{
                'new_user':new_user
            })
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html',
                  {
                      'user_form':user_form
                  })

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                  data=request.POST)
        profile_form = ProfileEditorForm(instance=request.user.profile,
                                         data=request.POST,
                                         files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return render(request, 'account/dashboard.html')
        else:
            messages.error(request, 'Error updating your profile')

            
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditorForm(instance=request.user.profile)
    
    return render(request,'account/edit.html',
                  {'user_form':user_form,
                   'profile_form':profile_form})
