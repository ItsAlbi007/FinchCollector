from django.shortcuts import render
# importing out calss based views (CBVs)
from django.views.generic.edit import CreateView

from .models import Finch

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
  
  return render(request, 'finch/detail.html', { 'finch': finch })

# inherit from CBV
class FinchCreate(CreateView):
  model = Finch
  fields = '__all__'
   # success_url = '/finch/{finch_id}'