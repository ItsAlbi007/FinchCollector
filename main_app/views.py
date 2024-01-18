import uuid
import boto3
import os

from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Finch, Toy, Photo
from .forms import FeedingForm



# define home view here - '/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# index view - shows all finch
def finch_index(request):
  finch = Finch.objects.all()

  return render(request, 'finch/index.html', { 'finch': finch })

# detail view - shows finch at '.finch/:id
def finch_detail(request, finch_id):
  finch = Finch.objects.get(id=finch_id)
  feeding_form = FeedingForm()
  return render(request, 'finch/detail.html', { 'finch': finch, 'feeding_form': feeding_form })

# inherit from CBV
class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'
   # success_url = '/finch/{finch_id}'
  
class FinchUpdate(UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class FinchDelete(DeleteView):
    model = Finch

    success_url = '/finch'

# FEEDING AND RELATIONSHIP VIEW FUNCTIONS
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', finch_id=finch_id)

class ToyList(ListView):
    model = Toy
    template_name = 'toys/index.html'

# ToyDetail
class ToyDetail(DetailView):
    model = Toy
    template_name = 'toys/detail.html'

# ToyCreate
class ToyCreate(CreateView):
    model = Toy
    fields = ['name', 'color']

    def form_valid(self, form):
        return super().form_valid(form)

# ToyUpdate
class ToyUpdate(UpdateView):
    model = Toy
    fields = ['name', 'color']
    
# ToyDelete
class ToyDelete(DeleteView):
    model = Toy
    success_url = '/toys'

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