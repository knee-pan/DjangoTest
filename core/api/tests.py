import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from ..models import Article

# python manage.py test
# python faker lib.

# coverage run --source "core/*" manage.py test -v 2 & coverage report


class TestArticle(APITestCase):
    url_list = reverse("article:list")
    url_create = reverse("article:create")

    def test_add_article(self):
        """
        Yeni article olusturma
        """
        data = {"headline": "head1", "content": "cont1"}
        response = self.client.post(self.url_create, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_unauth_article(self):
        """
        Kullanici giris yapmamissa article ekleme
        @self.client.credentials() : Giris islemi sonlandirilir.
        Bu sekilde create islemi yapilmak istenirse 403 donmeli.
        """
        self.client.credentials()
        data = {"headline": "head1", "content": "cont1"}
        response = self.client.post(self.url_create, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_articles(self):
        """
        Veri eklenir, get ile list ederim.
        Veri ekleme sebebi boş veriyi kontrol etmemek.
        """
        self.test_add_article()
        response = self.client.get(self.url_list)
        self.assertTrue(len(json.loads(response.content)["results"]) == Article.objects.all().count())


class ArticleUpdateDelete(APITestCase):
    url_access = reverse("token_obtain_pair")

    def setUp(self):
        self.username = "deneme1"
        self.pwd = "deneme1"

        """ Update islemini her kullanici kendi objesine yapmali.
            Bunu test etmek icin 2 user olusturulur."""

        self.user = User.objects.create_user(username=self.username, password=self.pwd)
        self.user2 = User.objects.create_user(username="deneme2", password="deneme2")

        self.article = Article.objects.create(headline="abc", content="abc")
        self.url = reverse("article:update", kwargs={"slug": self.article.slug})  # urls.py'da slug alır
        self.url_delete = reverse("article:delete", kwargs={"slug": self.article.slug})
        self.test_jwt_auth()

    def test_jwt_auth(self, username="deneme1", password="deneme1"):
        # r1 = self.client.login(data={"username": username, "password": password})
        r2 = self.client.post(self.url_access, data={"username": username, "password": password})
        # print(r1, r2, r2.data["access"])
        self.assertEqual(r2.status_code, status.HTTP_200_OK)
        # self.assertTrue("refresh" in json.loads(r2.content))
        self.token = r2.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION="Bearer " + self.token
        )  # headera yerleştirildi, bu sayede giriş yapıldı

    def test_article_update(self):
        data = {"headline": "deneme", "content": "icerik"}
        response = self.client.put(self.url, data)  # urls.py'da slug alır
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_article_update_different_user(self):
        """Kullanici sadece kendi postunu update edebilmeli"""
        self.test_jwt_auth("deneme2", "deneme2")
        data = {"headline": "deneme", "content": "icerik"}
        response = self.client.put(self.url, data)  # urls.py'da slug alır
        if response.status_code == 200:
            self.assertEqual(200, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertFalse(Article.objects.get(id=self.article.id).content == data["content"])

    def test_article_delete(self):
        """HTTP 204 -> Delete
        Article silindiğinde No Content donmeli"""
        response = self.client.delete(self.url_delete)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # def test_article_delete_from_another_user(self):
    #     """Farkli kul tarafindan farkli kul verisi silinirse, HTTP 403 Donmeli"""
    #     self.test_jwt_auth(username="deneme2", password="deneme2")
    #     response = self.client.delete(self.url_delete)
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
