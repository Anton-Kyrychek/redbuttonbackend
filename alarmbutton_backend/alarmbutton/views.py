from django.db import models
from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view
from .models import Customer, ButtonsEvents


@api_view(['POST'])
def button(request):
    try:
        customer = Customer.objects.get(registration_code=str(request.data['registration_code']))
    except Exception as e:
        return HttpResponse("No Person", 204)
    button_event = ButtonsEvents(
        customer=customer,
        caretaker=customer.caretaker,
        # comment=comment
        )
    button_event.save()

    customer.number_buttons_event = customer.number_buttons_event + 1
    customer.save()

    caretaker = customer.caretaker
    caretaker.number_buttons_received = caretaker.number_buttons_received + 1
    caretaker.save()
    return HttpResponse("OK")


@api_view(['POST'])
def reg_code_check(request):
    try:
        customer = Customer.objects.get(registration_code=str(request.data['registration_code']))
    except models.Model.DoesNotExist as e:
        return HttpResponse("No Person", 204)
    return JsonResponse({
        "first_name": customer.first_name,
        "last_name": customer.last_name,
        "birth_year": customer.birth_year,
    })
