from django.http import HttpResponse

# Create your views here.
def greeting_action(request):
    return HttpResponse('Hello, Kirill')
