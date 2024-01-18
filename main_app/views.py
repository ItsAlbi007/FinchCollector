import uuid
import boto3
import os

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Finch, Toy, Photo
from .forms import FeedingForm



# define home view here - '/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def finch_index(request):
  finch = Finch.objects.filter(user=request.user)
  return render(request, 'finch/index.html', { 'finch': finch })

@login_required
def finch_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  feeding_form = FeedingForm()
  return render(request, 'finch/detail.html', { 'finch': finch, 'feeding_form': feeding_form })

# inherit from CBV
class FinchCreate(LoginRequiredMixin, CreateView):
  model = Finch
  fields = ['name', 'breed', 'description', 'age']
   # success_url = '/finch/{finch_id}'
  
  def form_valid(self, form):
     form.instance.user = self.request.user
     return super().form_valid(form)
  
class FinchUpdate(LoginRequiredMixin, UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class FinchDelete(LoginRequiredMixin, DeleteView):
    model = Finch

    success_url = '/finch'

@login_required
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

class ToyList(LoginRequiredMixin, ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(LoginRequiredMixin, DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(LoginRequiredMixin, CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)

# ToyUpdate
class ToyUpdate(LoginRequiredMixin, UpdateView):
    model = Toy
    fields = ['name', 'color']
    
# ToyDelete
class ToyDelete(LoginRequiredMixin, DeleteView):
    model = Toy
    success_url = '/toys'

@login_required
def add_photo(request, finch_id):
   photo_file = request.FILES.get('photo-file', None)
   if photo_file:
      s3 = boto3.client('s3')
      key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
      try:
        bucket = os.environ['S3_BUCKET']
        s3.upload_fileobj(photo_file, bucket, key)
        url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
        Photo.objects.create(url=url, finch_id=finch_id)
      except Exception as e:
         print('An error occurred uploading file to S3')
         print(e)
      return redirect('detail', finch_id=finch_id)   
   
def signup(request):
  error_message = ''
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect ('index')
      else:
        error_message = 'Invalid sign up - try again'
        
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)