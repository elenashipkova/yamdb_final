from django.contrib import admin

from .models import User, Category, Comment, Genre, Review, Title
from users.models import RegistrationEmail


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class TitleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'year', 'description', 'category')
    search_fields = ('name', 'category')
    list_filter = ('genre', 'category')
    empty_value_display = '-пусто-'


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'title', 'score')
    search_fields = ('title',)
    list_filter = ('author',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'text', 'author', 'pub_date', 'review')
    search_fields = ('text',)
    list_filter = ('pub_date', 'author')


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'first_name', 'last_name',
                    'bio', 'role')
    search_fields = ('username',)
    list_filter = ('username', )
    empty_value_display = '-пусто-'


class RegistrationEmailAdmin(admin.ModelAdmin):
    list_display = ('pk', 'email', 'confirmation_code')
    search_fields = ('email',)
    empty_value_display = '-пусто-'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(RegistrationEmail, RegistrationEmailAdmin)
