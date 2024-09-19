from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import random

# Create your views here.
quotes = ["I don't like looking back. I'm always constantly looking forward. \
        I'm not the one to sort of sit and cry over spilt milk. I'm too busy looking for the next cow.",
        "That journey of coming back to the very top is better than actually being at the top. You find \
        out so much about yourself and who your friends are.",
        "Cooking is about passion, so it may look slightly temperamental in a way that it’s too assertive to the naked eye."
        ]

images = ["https://static.wikia.nocookie.net/hellskitchen/images/6/6f/Gordon_Ramsay.jpg/revision/latest?cb=20190118190638",
          "https://hips.hearstapps.com/hmg-prod/images/host-judge-gordon-ramsay-in-the-hells-kitchen-semi-finals-news-photo-1718650477.jpg",
          "https://media.timeout.com/images/105854659/image.jpg"]


def quote(request):
    # use this template to render the response
    template_name = 'quotes/quote.html'

    # create a dictionary of context variables for the template:
    context = {
        "quote" : random.choice(quotes),
        "image" : random.choice(images),
    }

    # delegate rendering work to the template
    return render(request, template_name, context)

def show_all(request):
    template_name = 'quotes/show_all.html'

    context = {
        "q1" : quotes[0],
        "q2" : quotes[1],
        "q3" : quotes[2],
        "i1" : images[0],
        "i2" : images[1],
        "i3" : images[2]
    }
    return render(request, template_name, context)

def about(request):
    template_name = 'quotes/about.html'

    context = {

    }

    return render(request, template_name, context)

