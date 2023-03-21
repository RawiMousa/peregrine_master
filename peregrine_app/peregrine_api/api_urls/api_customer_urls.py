from django.urls import path
from peregrine_app.peregrine_api.api_views import api_customer_views

app_name = "peregrine_app_api_customer_view"

urlpatterns = [

    # GET URLS
    path('api/customers/', api_customer_views.customer, name='customer'),

    # # POST/PATCH/DELETE URLS
    path('api/customers/<str:id>', api_customer_views.customer, name='customer')
]