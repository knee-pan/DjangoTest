import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Article

# python manage.py test
# python faker lib.


class TestArticle(APITestCase):
    url_list = reverse("article:list")
    url_create = reverse("article:create")

    def test_add_article(self):
        """
        Yeni article olusturma
        """
        data = {"headline": "head1", "content": "cont1", "author": self.request.user}
        response = self.client.post(self.url_create, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_unauth_article(self):
        """
        Kullanici giris yapmamissa article ekleme
        @self.client.credentials() : Giris islemi sonlandirilir.
        Bu sekilde create islemi yapilmak istenirse 403 donmeli.
        """
        self.client.credentials()
        data = {"headline": "head1", "content": "cont1", "author": self.request.user}
        response = self.client.post(self.url_create, data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_articles(self):
        """
        Veri eklenir, get ile list ederim.
        Veri ekleme sebebi boş veriyi kontrol etmemek.
        """
        self.test_add_article()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Article.objects.all().count())


class ArticleUpdateDelete(APITestCase):
    url_update = reverse("article:update")
    url_delete = reverse("article:delete")
    url_access = reverse("token_obtain_pair")

    def setUp(self):
        self.username = ""
        self.pwd = ""

        """ Update islemini her kullanici kendi objesine yapmali.
            Bunu test etmek icin 2 user olusturulur."""

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.user2 = User.objects.create_user(username="admin", password="admin")

        self.article = Article.objects.create(headline="", content="", author="")
        self.url = reverse("article:update", kwargs={"slug": self.article.slug})  # urls.py'da slug alır
        self.test_jwt_auth()

    def test_jwt_auth(self, username="", password=""):
        response = self.client.post(self.url_access, data={"username": username, "password": password})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in json.loads(response.content))
        self.token = response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.token
        )  # headera yerleştirildi, bu sayede giriş yapıldı

    def test_article_delete(self):
        """HTTP 204 -> Delete"""
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_article_delete_from_another_user(self):
        """KFarkli kul benim verimi silerse, HTTP 403 Donmeli"""
        self.test_jwt_auth("admin")
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_article_update(self):
        data = {"headline": "deneme", "content": "icerik", "author": self.request.user}
        response = self.client.put(self.url, data)  # urls.py'da slug alır
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_article_update_different_user(self):
        """Kullanici sadece kendi postunu update edebilmeli"""
        self.test_jwt_auth("staff11", "staff11")
        data = {"headline": "deneme", "content": "icerik", "author": self.request.user}
        response = self.client.put(self.url, data)  # urls.py'da slug alır
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertFalse(Article.objects.get(id=self.article.id).content == data["content"])
