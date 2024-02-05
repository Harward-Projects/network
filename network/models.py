from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


# If a user is followed by another ones, it means that those users are following this user.
class FollowState(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="the_user")
    followed_by = models.ManyToManyField(User, blank=True, related_name="followed_by")

    def __str__(self):
        return f"{self.user} is followed BY {self.followed_by}."


# A post has just one author and multiple likes from different users, if any. So, M2M field and blank:True
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)  # Charfield(max_lenght=255)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    like_count = models.PositiveSmallIntegerField(default=0)
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} posted a post."
