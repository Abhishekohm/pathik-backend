from django.shortcuts import render
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

app_name = "payment"


@csrf_exempt
def completePayment(request):
    if request.method == "POST":
        a = request.POST
        print(a)
        return render(request, 'success.html')
