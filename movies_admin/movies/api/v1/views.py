from movies.models import Filmwork, PersonRole
from django.http import JsonResponse
from django.views.generic.list import BaseListView
from django.views.generic.detail import BaseDetailView
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Q


class MoviesApiMixin:
    model = Filmwork
    http_method_names = ['get']

    def _aggregate_person(self, role: str):
        return ArrayAgg(
            'personfilmwork__person__full_name',
            filter=Q(personfilmwork__role=role),
            distinct=True,
        )

    def get_queryset(self):
        return FilmWork.objects.values('id', 'title', 'description', 'creation_date', 'rating', 'type'
                                       ).annotate(
            genres=ArrayAgg('genres__name', distinct=True),
            actors=self._aggregate_person(role=PersonRole.ACTOR),
            directors=self._aggregate_person(role=PersonRole.DIRECTOR),
            writers=self._aggregate_person(role=PersonRole.WRITER)
        )

    @staticmethod
    def render_to_response(context, **response_kwargs):
        return JsonResponse(context)


class MoviesListApi(MoviesApiMixin, BaseListView):
    paginate_by = 50

    def get_context_data(self, *, object_list=None, **kwargs):
        queryset = self.get_queryset()
        paginator, page, queryset, is_paginated = self.paginate_queryset(
            queryset,
            self.paginate_by
        )
        return {
            'count': paginator.count,
            'total_pages': paginator.num_pages,
            'prev': page.previous_page_number() if page.has_previous() else None,
            'next': page.next_page_number() if page.has_next() else None,
            'result': list(paginator.object_list),
        }


class MoviesDetailApi(MoviesApiMixin, BaseDetailView):

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)['object']
