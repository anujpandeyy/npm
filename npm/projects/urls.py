from . import views
from django.urls import path 

urlpatterns = [
    path("",views.Index),
    path("create/",views.CreateView),
    path("createSubmit/",views.Create),
    path("delete/<int:id>",views.Delete),
    path("edit/<int:id>",views.Edit),
    path("search/",views.Search),
    path("remarks/<int:id>",views.RemarksForm),
    path('contactus/',views.contactus),
    path('contactsubmit/',views.contactSubmit),

]