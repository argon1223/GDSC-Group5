from django.shortcuts import render
from .models import Subscription, add_subscription, delete_subscription

def add_subscription_button_onclick(request):
    if request.method == 'POST':
        add_subscription(request.POST.get('url'))

    subscriptions = Subscription.objects.all()

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'index.html', context)

def delete_subscription_button_onclick(request, pk):
    delete_subscription(pk)

    subscriptions = Subscription.objects.all()

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'index.html', context)