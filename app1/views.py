from django.shortcuts import render


def home(request):
    return render(request, 'app1/home.html')


def strategy01(request):
    return render(request, 'app1/strategy01.html')