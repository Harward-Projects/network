import json
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator

# from django.views.generic import ListView


from .models import User, Post
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

    # Employe paginator
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


def profile_view(request, user):
    return render(
        request,
        "network/profile.html",
        {
            "theuser": user,
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
