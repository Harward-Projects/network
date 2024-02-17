import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
    HttpResponseNotFound,
)
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator

from .models import User, Post, FollowState
from .forms import PostForm


@csrf_exempt
@login_required
def edit_post(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        data = json.loads(request.body)
        new_content = data.get("new_post_content")
        print(f"Edit Button:", new_content)
        post.content = new_content
        post.save()

        return JsonResponse({"message": "Post updated successfully."}, status=200)
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)
    # return redirect("index")


@login_required
def like_unlike_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        liked_state = data.get("liked")
        if (
            user in post.likes.all() and not liked_state
        ):  # double check if post was liked
            post.likes.remove(user)
        else:
            post.likes.add(user)
        post.save()
        print(f"PUT data:", data)
        print(f"liked:", data.get("liked"))

        return JsonResponse(
            {
                "message": "Post like/unlike state updated successfully.",
                "like_count": post.like_count(),
            },
            status=200,
        )
    else:
        return JsonResponse({"error": "Invalid request method."}, status=400)


def index(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save to DB
            post.author = request.user
            post.save()  # Now save to DB
            form = PostForm()
            # Redirect to the index page after form submission to prevent re-submission in refreshing page
            return redirect("index")
        else:
            form = PostForm()
    else:
        form = PostForm()

    # Order posts in reversed order based on creation_date
    posts = Post.objects.all().order_by("-creation_date")

    # Employ paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    num_pages_minus_two = page_obj.paginator.num_pages - 2

    return render(
        request,
        "network/index.html",
        {
            "form": form,
            "page_obj": page_obj,
            "num_pages_minus_two": num_pages_minus_two,
        },
    )


def follow_unfollow(user, current_user):
    try:
        # Check if there is a FollowState entry for the given user and current_user
        follow_state = FollowState.objects.get(user=user, followed_by=current_user)

        # If the current_user is already following the user, unfollow
        follow_state.followed_by.remove(current_user)
        return HttpResponse("Unfollowed successfully!")
    except FollowState.DoesNotExist:
        # If no FollowState entry exists, create a new one (follow)
        FollowState.objects.create(user=user, followed_by=current_user)
        return HttpResponse("Followed successfully!")


def profile_view(request, user):
    try:
        # Retrieve the user object by username
        user_obj = User.objects.get(username=user)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return HttpResponseNotFound("User not found")

    follow_state = None
    current_user = request.user
    try:
        # Try to retrieve the follow state
        follow_state = FollowState.objects.get(user=user_obj, followed_by=current_user)
    except ObjectDoesNotExist:
        # Handle the case where the FollowState object does not exist
        pass
    # follow_state = FollowState.objects.get(user=user_obj, followed_by=current_user)
    print("follow_state:", follow_state)
    # follow_unfollow(user, current_user)

    # Calculate the number of followers for the user
    followers_num = FollowState.objects.filter(user=user_obj).count()

    # Calculate the number of users that the current user is following
    following_num = FollowState.objects.filter(followed_by=user_obj).count()

    # Order the user's posts in reversed order based on creation_date
    posts = Post.objects.filter(author=user_obj).order_by("-creation_date")

    # Employ paginator
    paginator = Paginator(posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    num_pages_minus_two = page_obj.paginator.num_pages - 2

    return render(
        request,
        "network/profile.html",
        {
            "follow_state": follow_state,
            "followers_num": followers_num,
            "following_num": following_num,
            "page_obj": page_obj,
            "theuser": user,
            "num_pages_minus_two": num_pages_minus_two,
        },
    )


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
