from rest_framework import serializers

from ..models import Article, Comment, Company


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "company_type",
            "company_name",
            "company_employee_count",
            "country",
            "web_site",
            "company_employee_count",
        ]


class CompanyFilteredSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ["company_type", "company_name", "company_employee_count"]


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["headline", "pub_date", "content", "author", "slug"]


# eğer validateteki koşul sağlanmazsa iç içe yorumlar karışır.
class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        exclude = [
            "created",
        ]
        # fields = ["user", "article", "content", "parent", "created", "slug"]

    def validate(self, attrs):
        if attrs["parent"]:
            if attrs["parent"].article != attrs["article"]:
                raise serializers.ValidationError("something went wrong")
        return attrs


# İç içe yorum listeleme
class NestedCommentListSerializer(serializers.ModelSerializer):
    # replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ["user", "article", "content", "parent", "created", "slug"]

    def get_replies(self, obj):
        if obj.any_children:
            return NestedCommentListSerializer(obj.children(), many=True).data


# Yorum Listeleme & İç içe yorum listeleme ayrı
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class CommentDeleteUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["content"]
