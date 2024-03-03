from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone


# User = get_user_model()


class User(AbstractUser):
    pass
    # following = models.ManyToManyField(
    #     "self", blank=True, symmetrical=False, related_name="following"
    # )
    # followed_by = models.ManyToManyField(
    #     "self", blank=True, symmetrical=False, related_name="followed_by"
    # )

    def __str__(self):
        return self.username


# If a user is followed by another ones, it means that those users are following this user.
# class FollowState(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="the_user")
#     following = models.ManyToManyField(User, blank=True, related_name="following")
#     followed_by = models.ManyToManyField(User, blank=True, related_name="followed_by")

#     def __str__(self):
#         return f"{self.user} is followed BY {self.followed_by.all()[:5]}."

#     def follower_count(self):
#         return self.followed_by.count()


class Follow(models.Model):
    follower = models.ForeignKey(
        User, null=True, related_name="follower", on_delete=models.CASCADE
    )
    followed = models.ForeignKey(
        User, null=True, related_name="followed", on_delete=models.CASCADE
    )
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ["follower", "followed"]


# A post has just one author and multiple likes from different users, if any. So, M2M field and blank:True
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)  # Charfield(max_lenght=255)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} posted a post."

    def like_count(self):
        return self.likes.count()
