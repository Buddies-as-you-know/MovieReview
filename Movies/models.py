from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class TVAndMovie(models.Model):
    tmdb_id = models.IntegerField(
        verbose_name="",
        blank=False,
        null=False,
    )
    
    judge_tv_or_movie = models.CharField(
        blank=False, null=False, default="movie", max_length=20
    )
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )

    def get_comments(self) -> object:
        return Comment.objects.filter(
            tv_or_movie_id=self.id
        )

    def average_stars(self) -> float:
        comments = self.get_comments()
        n_comments = comments.count()
        if n_comments:
            self.stars = round(
                sum([comment.stars for comment in comments]) / n_comments, 3
            )
        else:
            self.stars = 0
        self.save()
        return self.stars

class Comment(models.Model):

    comment = models.TextField(max_length=1000)
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tv_or_movie = models.ForeignKey(TVAndMovie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("user", "tv_or_movie")
        indexes = [models.Index(fields=["user", "tv_or_movie"])]


class LikeForMovie(models.Model):

    movie = models.ForeignKey(TVAndMovie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class WantToSeeMovie(models.Model):
    movie = models.ForeignKey(TVAndMovie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class LikeForComment_movie(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
