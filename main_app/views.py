from django.shortcuts import render

# add finch list below 
# views.py

# Add this cats list below the imports
finch = [
  {'name': 'Haemorhous purpureus', 'breed': 'Fringillidae', 'description': 'Home Finch', 'age': 1},
  {'name': 'Red avadavat', 'breed': 'Estrildidae', 'description': 'Strawberry Finch', 'age': 2},
  {'name': 'Bicheno finch', 'breed': 'Taeniopygia bichenovii', 'description': 'Owl Finch', 'age': 0},  
]

# Create your views here.

# define home view here - '/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

# index view - shows all finch
def finch_index(request):
  return render(request, 'finch/index.html', { 'finch': finch })