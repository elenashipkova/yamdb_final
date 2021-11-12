from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from rest_framework.generics import (ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     DestroyAPIView)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser

from .filters import TitleFilterBackend
from .models import Category, Genre, Review, Title
from .permissions import IsOwnerOrStaffOrReadOnly, ReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class CommonListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ('name',)


class CategoriesListAPIView(CommonListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoriesDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'])


class GenreListAPIView(CommonListAPIView):
    serializer_class = GenreSerializer
    queryset = Genre.objects.all()


class GenreDetailAPIView(DestroyAPIView):
    permission_classes = [IsAdminUser]

    def get_object(self):
        return get_object_or_404(Genre, slug=self.kwargs['slug'])


class TitleListAPIView(ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Title.objects.all()
    filter_backends = [TitleFilterBackend]

    def get_serializer_class(self):
        return(
            TitleCreateSerializer if
            self.request.method == 'POST' else TitleSerializer)


class TitleDetailAPIView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ReadOnly]
    queryset = Title.objects.all()

    def get_serializer_class(self):
        return(
            TitleCreateSerializer if
            self.request.method in ['PATCH', 'PUT'] else TitleSerializer)


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsOwnerOrStaffOrReadOnly]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'),
                                   title=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review=review)
