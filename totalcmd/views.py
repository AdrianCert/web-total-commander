"""The module is dedicated to solving incoming requests"""
from django.http.request import HttpRequest
from django.shortcuts import render
from django.http import JsonResponse
from totalcmd.core import process


def home(request):
    """Home page for total commander

    Args:
        request (HttpRequest): the request that comes

    Returns:
        HttpResponse: Html page with the application itself
    """

    context = {
        'title': "Web Total Commander"
    }

    return render(request, 'totalcmd/index.html', context)


def action(request):
    """Take action on host based by dataForm

    Args:
        request (HttpRequest): the request that comes

    Returns:
        json: Json data which contains information about what happened
        in the action processing
    """
    assert isinstance(request, HttpRequest)
    assert request.method == "POST"
    return JsonResponse(process(request.POST.dict()))
