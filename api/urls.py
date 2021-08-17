from django.urls import path

from api.views import CurrencyDeltaViewSet, update_currencies

urlpatterns = [
    path('currency/<str:currency_code>/', CurrencyDeltaViewSet.as_view()),
    path('update/', update_currencies, name='get_update'),
]
