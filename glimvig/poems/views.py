from django.shortcuts import render

def home(request):

    

    return render(request, 'poems/home.html')

def about(request):
    return render(request, 'poems/about.html')

def poem_create(request):
    return render(request, 'poems/poem_create.html')

def poem_edit(request):
    return render(request, 'poems/poem_edit.html')

def poem_detail(request):
    return render(request, 'poems/poem_detail.html')

def profile_graph(request):
    return render(request, 'poems/profile_graph.html')

def search(request):
    return render(request, 'poems/search.html')