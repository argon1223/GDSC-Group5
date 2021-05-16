from os import name
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from homepage.views import home_page
from schedule.views import schedule_page
from subscription.views import subscription, add_subscription_button_onclick, delete_subscription_button_onclick

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_page),
    path('home/', home_page),
    path('video/', schedule_page),
    path('subscription/', subscription),
    path('subscription/add', add_subscription_button_onclick, name='Add'),
    path('subscription/remove/<str:pk>', delete_subscription_button_onclick, name='Delete')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
