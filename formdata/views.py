from django.shortcuts import render, redirect

# Create your views here.
def show_form(request):
    template_name= 'formdata/form.html'
    return render(request, template_name)

def submit(request):
    template_name = 'formdata/confirmation.html'

    print(request)

    #check to see if this is a POST (vs GET)
    if request.POST:
        # read the form data into python variables
        name = request.POST['name']
        favorite_color = request.POST['favorite_color']

        #package the data up to be used in the response
        context = {
            'name' : name,
            'favorite_color' : favorite_color
        }
        #generate a response
        return render(request, template_name, context=context)


    # how to handle if someone tries to directly go to submission page?
    #option 1: show the view of the form
    #template_name = 'formdata/form.html'
    #return render(request, template_name)

    #option 2:
    #return http response('nope')

    #option 2:redirect to correct url
    return redirect("show_form")