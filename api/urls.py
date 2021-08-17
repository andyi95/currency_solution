from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import CurrencyDeltaViewSet, ListCurrency, update_currencies

router = DefaultRouter()
router.register('', ListCurrency, basename='list-currency')

urlpatterns = [
    path('currency/<str:currency_code>/', CurrencyDeltaViewSet.as_view()),
    path('update/', update_currencies, name='get_update'),
    path('', include(router.urls)),
]
