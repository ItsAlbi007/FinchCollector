from django.shortcuts import render
# importing out calss based views (CBVs)
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Finch
from .forms import FeedingForm
# add finch list below 
# views.py

# Add this cats list below the imports
# this was to build the intial view - now we have finch in the db
#finch = [
#  {'name': 'Haemorhous purpureus', 'breed': 'Fringillidae', 'description': 'Home Finch', 'age': 1},
#  {'name': 'Red avadavat', 'breed': 'Estrildidae', 'description': 'Strawberry Finch', 'age': 2},
#  {'name': 'Bicheno finch', 'breed': 'Taeniopygia bichenovi', 'description': 'Owl Finch', 'age': 0},  
#]

# Create your views here.

# define home view here - '/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# index view - shows all finch
def finch_index(request):
  # collect out objects from teh database
  finch = Finch.objects.all()
  #print(finch)
  # for Finch in finch:
  #  print(finch)

  return render(request, 'finch/index.html', { 'finch': finch })

# detail view - shows finch at '.finch/:id
def finch_detail(request, finch_id):
  # find on finch with its id
  finch = Finch.objects.get(id=finch_id)
  feeding_form = FeedingForm()
  return render(request, 'finch/detail.html', { 'finch': finch, 'feeding_form': feeding_form })

# inherit from CBV
class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'
   # success_url = '/finch/{finch_id}'
  
class CatUpdate(UpdateView):
    model = Finch
    fields = ['breed', 'description', 'age']

# Delete View - extends DeleteView
class CatDelete(DeleteView):
    model = Finch

    success_url = '/cats'

# FEEDING AND RELATIONSHIP VIEW FUNCTIONS
def add_feeding(request, finch_id):
    form = FeedingForm(request.POST)
    if form.is_valid():
        new_feeding = form.save(commit=False)
        new_feeding.finch_id = finch_id
        new_feeding.save()
    return redirect('detail', cat_id=finch_id)