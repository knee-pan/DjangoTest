from django.db.models import Count
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    RetrieveDestroyAPIView,
    RetrieveUpdateAPIView,
)

from ..models import Article, Comment, Company
from .pagination import Pagination_
from .serializer import (
    ArticleSerializer,
    CommentCreateSerializer,
    CommentDeleteUpdateSerializer,
    CompanyFilteredSerializer,
    CompanySerializer,
    NestedCommentListSerializer,
)


class CompanyListAPI(ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = Pagination_


class CompanyFilteredListAPI(ListAPIView):
    serializer_class = CompanyFilteredSerializer
    pagination_class = Pagination_

    def get_queryset(self):
        query = (
            Company.objects.values("country").order_by("company_name").annotate(count=Count("company_employee_count"))
        )
        return query


class CompanyCreateAPI(CreateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    pagination_class = Pagination_
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["company_name"]
    ordering_fields = ["id"]


class CompanyDetailAPI(RetrieveAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"


class CompanyDestroyAPI(RetrieveDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class CompanyUpdateAPI(RetrieveUpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)


class ArticleListAPI(ListAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = Pagination_


class ArticleCreateAPI(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = Pagination_
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["headline"]
    ordering_fields = ["pub_date"]
    # permission_classes = [IsAuthenticated, IsAdminUser]

    # def perform_create(self, serializer):
    # serializer.save(author=self.request.user)


class ArticleDetailAPI(RetrieveAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = Pagination_
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "slug"


class ArticleDestroyAPI(RetrieveDestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = Pagination_
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "slug"

    def perform_destroy(self, instance):
        return super().perform_destroy(instance)


class ArticlePutAPI(RetrieveUpdateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = Pagination_
    # permission_classes = [IsAuthenticated, IsAdminUser]
    lookup_field = "slug"

    # def perform_update(self, serializer):
    # serializer.save(author=self.request.user)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class NestedCommentListAPIView(ListAPIView):
    # queryset = Comment.objects.all()
    serializer_class = NestedCommentListSerializer

    def get_queryset(self):
        return Comment.objects.filter(parent=None)
        # queryset = Comment.objects.filter(parent=None)
        # query = self.request.GET.get("q")
        # if query:
        #     query = queryset.filter(article=query)
        # return query


class CommentUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CommentDeleteAPIView(RetrieveDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteUpdateSerializer
    lookup_field = "pk"
