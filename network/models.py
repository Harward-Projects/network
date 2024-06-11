from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

    def __str__(self):
        return self.username


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

    # def follower_count(self):
    #     return self.follower.count()

    # def following_count(self):
    #     return self.followed.count()

    def follow_state(self):
        return f"{self.follower.username} follows {self.followed.username}."


# A post has just one author and multiple likes from different users, if any. So, M2M field and blank:True
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(blank=False)  # Charfield(max_lenght=255)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    creation_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} posted a post in {self.creation_date}."

    def like_count(self):
        return self.likes.count()
