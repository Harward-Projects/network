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

from .models import User, Post, Follow
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
            "related": "All",
            "form": form,
            "current_view": "index",
            "view_param": None,
            "page_obj": page_obj,
            "num_pages_minus_two": num_pages_minus_two,
        },
    )


@login_required
def following_view(request):
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

    # Gather posts from followers
    posts = Post.objects.none()  # Initialize an empty queryset
    followers = Follow.objects.filter(follower=request.user)
    for follower in followers:
        print(f"followers of {request.user} are:", follower.followed.username)
    for follower in followers:
        follower_posts = Post.objects.filter(author=follower.followed)
        posts = posts.union(follower_posts)
        for post in posts:
            print(post.author.username)
    followers_posts = posts.order_by("-creation_date")

    # Employ paginator
    paginator = Paginator(followers_posts, 10)
    page_number = request.GET.get("page", 1)
    page_obj = paginator.get_page(page_number)
    num_pages_minus_two = page_obj.paginator.num_pages - 2

    return render(
        request,
        "network/index.html",
        {
            "related": "Following",
            "form": form,
            "current_view": "following",
            "view_param": None,
            "page_obj": page_obj,
            "num_pages_minus_two": num_pages_minus_two,
        },
    )


def profile_view(request, theuser):
    current_user = request.user

    try:
        # Retrieve the user object by username
        theuser_obj = User.objects.get(username=theuser)
    except User.DoesNotExist:
        # Handle the case where the user does not exist
        return HttpResponseNotFound("User not found")

    # follow_state = "not defined"
    if current_user.is_authenticated:
        try:
            follow_obj = Follow.objects.get(follower=current_user, followed=theuser_obj)
            follow_state = True
            print("try follow_state:", follow_state)
            followers_num = Follow.objects.filter(followed=theuser_obj).count()
            print("THE TRY followers_num count():", followers_num)
        except:
            follow_state = False
            print("except follow_state:", follow_state)
    else:
        follow_state = None

    print("theuser_obj:", theuser_obj)
    user = User.objects.get(username=theuser_obj)
    print("user:", user)
    print("current_user:", current_user)

    follower_state = Follow.objects.all().filter(followed=theuser_obj)
    followed_state = Follow.objects.all().filter(follower=theuser_obj)
    print("theuser_obj.id", theuser_obj.id)
    print("follower_state.all()", follower_state),
    print("follow_state.followed_by.all()", followed_state)
    followers_num = follower_state.count()
    print("followers_num:", followers_num)
    following_num = followed_state.count()
    print("following_num:", following_num)

    # Order the user's posts in reversed order based on creation_date
    posts = Post.objects.filter(author=theuser_obj).order_by("-creation_date")

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
            "current_view": "profile",
            "view_param": theuser,
            "page_obj": page_obj,
            "theuser": theuser,
            "num_pages_minus_two": num_pages_minus_two,
        },
    )


@login_required
def follow_unfollow(request, theuser):
    current_user = request.user
    theuser_obj = get_object_or_404(User, username=theuser)

    if request.method == "PUT":
        try:
            # Check if there is a FollowState entry for the given user and current_user
            follow_state = Follow.objects.get(
                follower=current_user, followed=theuser_obj
            )
            print("theuser_follow_state before remove:", follow_state)

            # If the current_user is already following the user, unfollow
            follow_state.delete()
            print("theuser_follow_state aftere remove:", follow_state)

            return HttpResponse("Unfollowed successfully!", {})

        except Follow.DoesNotExist:
            # If no FollowState entry exists, create a new one (follow)
            follow_state = Follow.objects.create(
                follower=current_user, followed=theuser_obj
            )
            print("theuser_follow_state after create:", follow_state)
            return HttpResponse("Followed successfully!")

    return HttpResponse("Invalid request method")


@login_required
def like_unlike_post(request, post_id):
    user = request.user
    post = get_object_or_404(Post, pk=post_id)
    if request.method == "PUT":
        data = json.loads(request.body)
        liked_state = data.get("liked")
        if user in post.likes.all() and not liked_state:
            # liked_state double checks if post was liked (excesive)
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
                {
                    "message": "Invalid username and/or password.",
                    "current_view": "login",
                    "view_param": None,
                },
            )
    else:
        return render(
            request,
            "network/login.html",
            {
                "current_view": "login",
                "view_param": None,
            },
        )


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
                request,
                "network/register.html",
                {
                    "message": "Passwords must match.",
                    "current_view": "register",
                    "view_param": None,
                },
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "network/register.html",
                {
                    "message": "Username already taken.",
                    "current_view": "register",
                    "view_param": None,
                },
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(
            request,
            "network/register.html",
            {
                "current_view": "register",
                "view_param": None,
            },
        )
