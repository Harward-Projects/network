from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("allPosts", views.allPosts, name="allPosts"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # network(Poster) API routes
    # path("", views.???, name="???"),
]
