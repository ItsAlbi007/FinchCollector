from django.shortcuts import render

# Create your views here.

# define home view here - '/'

def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')