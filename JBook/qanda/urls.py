"""jbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from qanda.views import *
app_name = 'qanda'
urlpatterns = [

    path('',index1, name = 'index_qanda'),
    path('question/<int:qid>/<slug:qslug>/',view_question ,name = 'view_question'),
    path('ask_ques/',ask_ques, name = "ask_ques"),
<<<<<<< HEAD
    path('ajax-answer-question',ajaxanswerquestion),

=======
>>>>>>> a10ac16d12d91a4ffa244062ce2eded530c5f64a

]
