from django.urls import path
from .views import search, start_page


urlpatterns = [
    path('form_submit', search, name='form_submit'),
    path('', start_page, name='start_page')
]
