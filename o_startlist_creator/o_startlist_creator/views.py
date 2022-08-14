from django.http import HttpResponse


def hello(request, name):
    return HttpResponse(f"<h2>Hello {name}</h2>")