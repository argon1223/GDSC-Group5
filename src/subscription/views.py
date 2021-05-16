from django.shortcuts import render, redirect
from .models import Subscription, add_subscription, delete_subscription

def subscription(request):
    subscriptions = Subscription.objects.all()

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'subscription_page.html', context)


def add_subscription_button_onclick(request):
    if request.method == 'POST':
        add_subscription(request.POST.get('suburl'))
        return redirect('../subscription')

    subscriptions = Subscription.objects.all()

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'subscription_page.html', context)


def delete_subscription_button_onclick(request, pk):
    if request.method == 'POST':
        delete_subscription(pk)
        return redirect('../../subscription')

    subscriptions = Subscription.objects.all()

    context = {
        'subscriptions': subscriptions,
    }

    return render(request, 'subscription_page.html', context)