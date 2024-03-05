from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    # network(Poster) API routes
    path("profile/<str:theuser>", views.profile_view, name="profile"),
    path("following", views.following_view, name="following"),
    path(
        "profile/<str:theuser>/follow",
        views.follow_unfollow,
        name="follow_unfollow_theuser",
    ),
    path("post/<int:post_id>/edit/", views.edit_post, name="edit_post"),
    path("post/<int:post_id>/like/", views.like_unlike_post, name="like_unlike_post"),
]
