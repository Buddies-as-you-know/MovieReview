from accounts.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import CheckConstraint, Q, Sum
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
        default=0.00,
        validators=[MinValueValidator(0.0), MaxValueValidator(10.0)],
    )

    def average_stars(self) -> float:
        count = self.comment_set.count()
        if count:
            get_sum = self.comment_set.aggregate(Sum("stars"))
            self.stars = round(get_sum["stars__sum"] / count, 3)
        else:
            self.stars = 0.00
        self.save()
        return self.stars
        """
        self.stars = round(self.comment_set.aggregate(Avg('stars')).get('stars__avg'), 3)
        self.save()
        return self.stars or 0
        """


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
        constraints = (
            # for checking in the DB
            CheckConstraint(
                check=Q(stars__gte=0.0) & Q(stars__lte=10.0), name="cooment_stars_range"
            ),
        )


class LikeForMovieAndTV(models.Model):

    movie = models.ForeignKey(TVAndMovie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class WantToSeeMovieAndTV(models.Model):
    movie = models.ForeignKey(TVAndMovie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)


class LikeForComment(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)
