from django.shortcuts import render

# Create your views here.


# FAQ templatate view
def faq(request):
    """ View that renders faq template """

    return render(request, 'public/faq.html')


# Feedback templatate view
def feedback(request):
    """ View that renders feedback template """

    return render(request, 'public/feedback.html')
