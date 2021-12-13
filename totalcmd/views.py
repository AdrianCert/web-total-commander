from django.shortcuts import render
from django.shortcuts import render

def home(request):

    context = {
        'title': "Web Total Commander"
    }

    return render(request, 'totalcmd/index.html', context)
