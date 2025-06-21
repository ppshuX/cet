from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def listening(request):
    return render(request, 'listening.html')

def reading(request):
    return render(request, 'reading.html')

def writing(request):
    return render(request, 'writing.html')

def translate(request):
    return render(request, 'translate.html')

def travel(request):
        return render(request, 'travel.html')
