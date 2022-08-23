import random

from accounts.models import CustomUser
from django.test import TestCase

from Movies.models import Comment, TVAndMovie


class CommentModelTests(TestCase):
    def test_is_empty(self):
        """初期状態では何も登録されていないことをチェック"""
        saved_comments = Comment.objects.all()
        self.assertEqual(saved_comments.exists(), False)


class TVAndMovieTests(TestCase):
    def test_is_empty(self):
        empty_tv_or_movie = TVAndMovie.objects.all()
        self.assertEqual(empty_tv_or_movie.exists(), False)
        self.assertNotEqual(empty_tv_or_movie.count(), 1)

    def test_is_one_create(self):
        one_tv_or_movie = TVAndMovie.objects.create(
            tmdb_id=200, judge_tv_or_movie="movie", stars=2.22222222222222222222
        )
        self.assertEqual(one_tv_or_movie.tmdb_id, 200)
        self.assertEqual(one_tv_or_movie.judge_tv_or_movie, "movie")
        self.assertEqual(one_tv_or_movie.stars, 2.22222222222222222222)

    def test_is_average_star(self):
        obj_test_movie_and_test = TVAndMovie.objects.create(
            tmdb_id=200, judge_tv_or_movie="movie", stars=2.22222222222222222222
        )
        create_user_list = [
            CustomUser(
                email="test{}@example.com".format(i),
            )
            for i in range(0, 100000)
        ]
        CustomUser.objects.bulk_create(create_user_list)
        create_comment_list = [
            Comment(
                comment="Test-{}".format(i),
                stars=random.uniform(0, 10),
                user=create_user_list[i],
                tv_or_movie=obj_test_movie_and_test,
            )
            for i in range(0, 100000)
        ]
        Comment.objects.bulk_create(create_comment_list)
        average_score_test = obj_test_movie_and_test.average_stars()
        self.assertEqual(len(create_comment_list), 100000)
        self.assertLessEqual(average_score_test, 10.0)
        self.assertGreaterEqual(average_score_test, 0.0)
        print(average_score_test)

        def no_comment_get_average_score(self):
            obj_test_movie_and_test = TVAndMovie.objects.create(
                tmdb_id=201, judge_tv_or_movie="movie"
            )
            average_score_test = obj_test_movie_and_test.average_stars()
            print(average_score_test)
