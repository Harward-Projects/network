from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # network(Poster) API routes
    path("profile/<str:user>", views.profile_view, name="profile"),
    path("post/<int:post_id>", views.edit_post, name="edit_post"),
]
