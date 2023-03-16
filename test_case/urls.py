from django.urls import path
from .views import search, start_page
from test_case.api.views import CSVAPIView


urlpatterns = [
    path('form_submit', search, name='form_submit'),
    path('', start_page, name='start_page'),
    path('api/v1/csv', CSVAPIView.as_view())
]
