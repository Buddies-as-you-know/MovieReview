import requests
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from Tmdb_api_key import TMDB_API_KEY


class CreateSearchAndReturnTVOrMovie:
    def __init__(
        self,
        tv_or_movie_judge: str,
        tv_or_movie_object: object = None,
        inputs_request=None,
        tmdb_api_key: str = TMDB_API_KEY,
    ) -> None:
        self.judge_tv_or_movie = tv_or_movie_judge
        self.object_tv_or_movie = tv_or_movie_object
        self.inputs_request = inputs_request
        self.tmdb_api_key = tmdb_api_key
    
    def score_by_data_format_save(self) -> None:
        min_score_query: float = 0
        max_score_query: float = 10
        if self.inputs_request.GET.get("min") and self.inputs_request.GET.get("max"):
            min_score_query = self.inputs_request.request.GET.get("min")
            max_score_query = self.inputs_request.request.GET.get("max")
        self.tv_or_movie_list: list = []
        if self.object_tv_or_movie.exists():
            for tmp_obj in self.object_tv_or_movie:
                if (min_score_query <= tmp_obj.average_stars()) and (
                    max_score_query >= tmp_obj.average_stars()
                ):
                    tv_or_movie_url: str = (
                        "https://api.themoviedb.org/3/" +
                        self.judge_tv_or_movie +
                        "/" +
                        tmp_obj.id +
                        "?api_key=" +
                        self.tmdb_api_key +
                        "&language=en-US"
                    )
                    data: dict = (requests.get(tv_or_movie_url)).json()
                    data["score"] = tmp_obj.average_stars()
                    self.tv_or_movie_list.append(data)

    def search_data(self, query) -> dict:
        data_search: dict = (requests.get(
            f"https://api.themoviedb.org/3/search/{self.__request.GET.get('type')}?api_key={self.__tmdb_api_key}&language=en-US&page=1&include_adult=false&query={query}"
        )).json()
        
        search_context = {"search_data": data_search, "type": self.inputs_request.GET.get('type')}
        
        return search_context

    def pagitor_deliver(self, page_number, html_page_tag="page"):
        paginator = Paginator(self.tv_or_movie_list, page_number)
        page = self.inputs_request.GET.get(html_page_tag, 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
        return pages
