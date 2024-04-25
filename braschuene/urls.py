from django.urls import path
from django.conf import settings
from braschuene import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_debt", views.add_debt, name="add_debt"),
    path("debt_done/<int:id>", views.done, name="done"),
    path("debt_double/<int:id>", views.double, name="double"),
]
