from django.urls import path

from .views import (
    ArticleCreateAPI,
    ArticleDestroyAPI,
    ArticleDetailAPI,
    ArticleListAPI,
    ArticlePutAPI,
    CommentCreateAPIView,
    CommentDeleteAPIView,
    CommentUpdateAPIView,
    CompanyCreateAPI,
    CompanyDestroyAPI,
    CompanyDetailAPI,
    CompanyListAPI,
    CompanyUpdateAPI,
    NestedCommentListAPIView,
)

# "{% url 'root:detail' question.id %}"
app_name = "article"
urlpatterns = [
    # Home page.
    path("list_comp", CompanyListAPI.as_view(), name="list_comp"),
    path("create_comp", CompanyCreateAPI.as_view(), name="create_comp"),
    path("detail_comp/<pk>", CompanyDetailAPI.as_view(), name="detail_comp"),
    path("update_comp/<pk>", CompanyUpdateAPI.as_view(), name="update_comp"),
    path("delete_comp/<pk>", CompanyDestroyAPI.as_view(), name="delete_comp"),
    path("list", ArticleListAPI.as_view(), name="list"),
    path("create", ArticleCreateAPI.as_view(), name="create"),
    path("detail/<slug>", ArticleDetailAPI.as_view(), name="detail"),
    path("update/<slug>", ArticlePutAPI.as_view(), name="update"),
    path("delete/<slug>", ArticleDestroyAPI.as_view(), name="delete"),
    path("comment/nested_list", NestedCommentListAPIView.as_view(), name="nested_list"),
    path("comment/createview", CommentCreateAPIView.as_view(), name="comment_create_view"),
    path("com/update/<pk>", CommentUpdateAPIView.as_view(), name="com_update"),
    path("com/delete/<pk>", CommentDeleteAPIView.as_view(), name="com_delete"),
]
