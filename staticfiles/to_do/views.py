from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import UserProfile, Task
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView, CreateView, DetailView, UpdateView, DeleteView
)
from django.contrib.auth.decorators import login_required
from .forms import NewTakForm
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.views import PasswordChangeView, PasswordChangeForm
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Task
from datetime import datetime, timedelta, timezone

@shared_task
def check_task_due_dates():
    # Get tasks that are due within the next 24 hours
    tasks = Task.objects.filter(happening_on__gt=timezone.now(), happening_on__lte=timezone.now() + timedelta(days=1))

    # Loop through tasks and send email to user
    for task in tasks:
        # Render email template with task details
        context = {'task': task}
        html_message = render_to_string('task_dues/task_due.html', context)

        # Send email to user
        send_mail(
            subject=f'Task due: {task.title}',
            message='',
            from_email='groupassignmentemail301@gmail.com',
            recipient_list=[task.user.email],
            html_message=html_message
        )

# check_task_due_dates.delay()

class PasswordsChangeView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('home')

    success_message = "Password successfully changed...!"
    login_url = 'signin'

def go_back(request):
    previous_page = request.META.get('HTTP_REFERER')
    return HttpResponseRedirect(previous_page)

def success_onDelete(request):
    return render(request, 'app_pages/confirmed_deletion.html')

class TaskDetail(DetailView):
    model = Task
    template_name='app_pages/task_details.html'

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('confirm_deletion')

    template_name = 'app_pages/confirm_delete_task.html'

class UpdateTask(SuccessMessageMixin, UpdateView):
    model = Task
    template_name = "app_pages/update_task.html"

    fields = [
        'title', 'description', 'happening_on', 'completed'
    ]

    success_message = "Task successfully updated...!"

class UpdateProfile(SuccessMessageMixin, UpdateView):
    model = UserProfile
    template_name = "app_pages/update_profile.html"

    fields = [
        'first_name', 'surname', 'date_of_birth', 'about_me', 'physical_address', 'profile_photo'
    ]

    success_message = "Profile successfully updated...!"


@login_required(login_url='signin')
def home(request):
    task = Task.objects.filter(user=request.user)
    # tasks = Task.objects.all
    task = task.order_by('happening_on').first()

    context = {
        'task': task,
    }

    return render(request, 'app_pages/index.html', context)

def alltasks(request):
    tasks = Task.objects.filter(user=request.user)
    # tasks = Task.objects.all

    context = {
        'tasks': tasks,
    }

    return render(request, 'app_pages/alltasks.html', context)


@login_required(login_url='signin')
def account_settings(request, pk):
    user_profile = UserProfile.objects.get(id=pk)

    context = {
        messages: 'messages',
        'user_profile': user_profile,
    }
    return render(request, 'app_pages/account_settings.html', context)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email_address = request.POST['email_address']
        surname = request.POST['surname']
        first_name = request.POST['first_name']
        date_of_birth = request.POST['date_of_birth']
        password = request.POST['password']

        myUser = UserProfile.objects.create_user(
            email_address, username, password)

        myUser.date_of_birth = date_of_birth
        myUser.first_name = first_name
        myUser.surname = surname

        myUser.is_personal = True
        myUser.is_active = True

        myUser.save()
        messages.success(request, "Personal account created Successfully...!")

        return redirect("signin")
    # else:
    #     messages.error(request, "Passwords don't Match")
    #     return redirect("signup")

    context = {
        messages: 'messages'
    }
    return render(request, 'app_pages/signup.html')


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        this_user = authenticate(username=username, password=password)

        if this_user is not None:
            login(request, this_user)
            messages.success(request, 'Logged In')
            return redirect('home')

        else:
            messages.error(request, 'Invalid Credentials')
            return redirect('signin')
    
    def get_success_url(self):
        next_url = self.request.GET.get('next')
        if next_url:
            return next_url
        else:
            return '/'

    return render(request, 'app_pages/signin.html')


@login_required(login_url='signin')
def signout(request):
    logout(request)
    messages.info(request, 'Logged Out..!')
    return redirect('signin')


@login_required(login_url='signin')
def new_task(request):
    return render(request,)


class NewTask(SuccessMessageMixin, CreateView):
    model = Task
    form_class = NewTakForm
    template_name = 'app_pages/new_task.html'

    success_message = "Task added successfully"

    def form_valid(self, NewTaskForm):
        NewTaskForm.instance.user = self.request.user
        return super().form_valid(NewTaskForm)