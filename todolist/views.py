import datetime
from django.urls import reverse
from todolist.models import Task
from todolist.forms import FormTask
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# show todolist
@login_required(login_url='/todolist/login/')
def show_todolist(request):
  tasks = Task.objects.filter(user=request.user)
  context = {
      'username': request.user.username,
      'tasks': tasks,
  }
  return render(request, "todolist_home.html", context)

# register
def register(request):
  form = UserCreationForm()
  if request.method == "POST":
      form = UserCreationForm(request.POST)
      if form.is_valid():
          form.save()
          messages.success(request, 'Akun telah berhasil dibuat!')
          return redirect('todolist:login')
  context = {'form':form}
  return render(request, 'register.html', context)

# login
def login_user(request):
  if request.method == 'POST':
      username = request.POST.get('username')
      password = request.POST.get('password')
      user = authenticate(request, username=username, password=password)
      if user is not None:
          login(request, user)
          response = HttpResponseRedirect(reverse("todolist:show_todolist"))
          response.set_cookie('last_login', str(datetime.datetime.now()))
          return response
      else:
          messages.info(request, 'Username atau Password salah!')
  context = {}
  return render(request, 'login.html', context)

# logout
def logout_user(request):
  logout(request)
  response = HttpResponseRedirect(reverse('todolist:login'))
  response.delete_cookie('last_login')
  return response

# create task
@login_required(login_url='/todolist/login/')
def create_task(request):
  if request.method == "POST":
    form = FormTask(request.POST)
    if form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        Task.objects.create(user=request.user, date=datetime.datetime.now(), title=title, description=description)
        return redirect('todolist:show_todolist')
  else:
    form = FormTask()
  return render(request, "create_task.html", context={"form": form})

# delete
@login_required(login_url='/todolist/login/')
def delete(request, id):
  task = Task.objects.get(id=id)
  task.delete()
  return redirect('todolist:show_todolist')

#change status
@login_required(login_url='/todolist/login/')
def change_status(request, id):
  task = Task.objects.get(id=id)
  task.is_finished = not (task.is_finished)
  task.save()
  return redirect('todolist:show_todolist')