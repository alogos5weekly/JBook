from django.contrib import admin
from django.urls import path
from qanda.views import *

app_name = 'qanda'

urlpatterns = [
    path('', index),
    path('question/<int:qid>/<slug:qslug>/', viewquestion, name='view-question'),
    path('ask-question/', askquestion, name='ask-question'),
]
