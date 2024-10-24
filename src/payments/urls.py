from django.urls import path
from .views import TossPaymentView, UserPaymentListView

urlpatterns = [
    path('toss/', TossPaymentView.as_view(), name='toss-payment'),
    path('my/', UserPaymentListView.as_view(), name='my-payments'),
]
