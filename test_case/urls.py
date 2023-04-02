from django.urls import path
from .views import search, start_page
from test_case.api.views import API_View

urlpatterns = [
    path('form_submit', search, name='form_submit'),
    path('', start_page, name='start_page'),
    path('api/v1/csv', API_View.as_view())
]
