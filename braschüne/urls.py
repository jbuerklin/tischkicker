"""
URL configuration for tischkicker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path

from braschüne import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('goal-button/<str:side>', views.goalButton, name='goal-button'),

    path("add-player/<str:side>/<int:playerId>", views.addPlayer, name="add-player"),
    path("remove-player/<str:side>/<int:playerId>", views.removePlayer, name="remove-player"),
    path("swap-players/<str:side>", views.swapPlayers, name="swap-players"),
    path("goal/<str:side>", views.goal, name="swap-players"),
    path("next-round", views.nextRound, name="next-round"),
    path("end-game", views.endGame, name="end-game"),
    path("sse", views.sse, name="sse"),

    path("done-beer/<int:beerId>", views.doneBeer, name="done-beer"),
    path("delete-beer/<int:beerId>", views.deleteBeer, name="delete-beer"),

    path("accounts/profile/", views.ProfileView.as_view(), name="profile"),
    path("profile-events", views.profile_events, name="profile-events"),
]
