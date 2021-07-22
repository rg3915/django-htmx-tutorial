from django.urls import path

from backend.state import views as v

app_name = 'state'


urlpatterns = [
    path('', v.state_list, name='state_list'),
    path('uf/', v.uf_list, name='uf_list'),
    path('result/', v.state_result, name='state_result'),
]
