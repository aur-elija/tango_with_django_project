from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    #Construct a dictionary to pass to the template engine as its context
    context_dict = {'boldmessage': "Crunchy, creamy, cookie, candy, cupacke!"}
    #return a rendered response to send to the client
    #first param is the template we wish to use
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    #return HttpResponse("Rango says here is the about page <br/>"
    #                    "<a href='/rango/'>Index</a>")
    context_dict = {}
    return render(request, 'rango/about.html', context=context_dict)
