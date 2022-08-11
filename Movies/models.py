from accounts.models import CustomUser
from django.core.validators import (MaxValueValidator, MinValueValidator,
                                    RegexValidator)
from django.db import models
from django.utils import timezone

alphanumeric = RegexValidator(r"^[0-9]*$",
                              "Only alphanumeric characters are allowed.")


class Movie(models.Model):
    id = models.CharField(
        primary_key=True,
        editable=False,
        validators=[alphanumeric],
        max_length=9999
    )
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )

    def get_comments(self):
        return Comment_movie.objects.filter(movie_id=self.id)

    def average_stars(self):
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


class TV(models.Model):
    id = models.CharField(
        primary_key=True,
        editable=False,
        validators=[alphanumeric],
        max_length=9999
    )
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )

    def get_comments(self):
        return Comment_tv.objects.filter(tv_id=self.id)

    def average_stars(self):
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


class Comment_movie(models.Model):
    comment = models.TextField(max_length=1000)
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]

    class Meta:
        unique_together = ("user", "movie")
        indexes = [models.Index(fields=["user", "movie"])]


class Comment_tv(models.Model):

    comment = models.TextField(max_length=1000)
    stars = models.FloatField(
        blank=False,
        null=False,
        default=0,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    tv = models.ForeignKey(TV, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.comment[:20]

    class Meta:
        unique_together = ("user", "tv")
        indexes = [
            models.Index(fields=["user", "tv"]),
        ]


class LikeForMovie(models.Model):
    """Movieに対するいいね"""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.timestamp


class LikeForTV(models.Model):
    """TVに対するいいね"""

    tv = models.ForeignKey(TV, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)


class WantToSeeMovie(models.Model):
    """Movieに対するみたい"""

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)


class WantToSeeTV(models.Model):
    """TVに対するみたい"""

    tv = models.ForeignKey(TV, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)


class LikeForComment_movie(models.Model):
    """Movieコメントに対するいいね"""

    comment = models.ForeignKey(Comment_movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)


class LikeForComment_tv(models.Model):
    """TVコメントに対するいいね"""

    comment = models.ForeignKey(Comment_tv, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.timestamp)
