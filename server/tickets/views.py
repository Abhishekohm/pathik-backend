from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from locations.models import Location
from .serializers import TicketSerializer
from .models import Ticket
from django.conf import settings

# Create your views here.
import razorpay


@api_view(['GET', 'POST'])
def bookTicket(request):
    if request.method == "POST":
        data = ({
            'user': User.objects.get(username=request.POST.get('user')).pk,
            'location': Location.objects.get(name=request.POST.get('location')).pk,
            'date': request.POST.get('date'),
            'quantity': request.POST.get('quantity'),
            'amount': request.POST.get('amount'),
        })
        ticket = TicketSerializer(data=data)
        if ticket.is_valid():
            ticket.save()
            # Getting all the items from the frontend after validation
            user = User.objects.get(username=request.POST.get('user'))
            location = Location.objects.get(name=request.POST.get('location'))
            date = request.POST.get('date')
            quantity = request.POST.get('quantity')
            amount = request.POST.get('amount')

            # Creating Razorpay Client and Order id
            client = razorpay.Client(
                auth=(settings.RAZORPAY_PUBLIC_KEY, settings.RAZORPAY_SECRET_KEY))

            payment = client.order.create(
                {'amount': int(amount)*100, 'currency': 'INR', 'payment_capture': '1'})

            print(payment)

            # Saving everything in the Ticket Model
            tempTicket = Ticket(user=user, location=location,
                                date=date, quantity=quantity, amount=amount, payment_id=payment['id'])
            tempTicket.save()

            Payment = {
                'KEY_ID': settings.RAZORPAY_PUBLIC_KEY,
                'id': payment['id'],
                'amount': payment['amount'],
            }

            return render(request, 'payment.html', {'Payment': Payment})

        return Response(ticket.errors)
    else:
        return render(request, 'form.html')
