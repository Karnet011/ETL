from django.contrib import admin
from .models import Filmwork, GenreFilmWork, Genre, Person, PersonFilmWork


class GenreFilmworkTabularInline(admin.TabularInline):
    model = GenreFilmWork


class PersonFilmWorkTabularInline(admin.TabularInline):
    model = PersonFilmWork


class FilmWorkAdmin(admin.ModelAdmin):
    inlines = [GenreFilmworkTabularInline, PersonFilmWorkTabularInline]
    model = Filmwork
    list_display = ('title', 'type', 'creation_date', 'rating')
    fields = (
        'title', 'type', 'description', 'creation_date', 'certificate',
        'file_path', 'rating',
    )

    list_filter = ('type',)

    search_fields = ('title', 'description', 'id')


admin.site.register(Filmwork, FilmWorkAdmin)
admin.site.register(Genre)
admin.site.register(Person)
