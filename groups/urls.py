from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('thanks/', views.thanks, name='thanks'),
    path('create/nothanks/', views.nothanks, name='nothanks'),
    path('join/', views.join, name='join'),
    path('party/<int:party_id>', views.partyview, name='party') #change to slug for party name instead of id
]