# user sign up test

import json

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# APITestCase , self.client ile APIClient tetikler.
# python manage.py test
# test çalıştırıldığında arkada bir test db oluşturuluyor ve işlemler bittiğinde
# test db siliniyor


# datayı python Faker kütüphanesi kullanarak düzenle


class TestUserRegister(APITestCase):
    url = reverse("account:register")
    url_access = reverse("token_obtain_pair")

    def test_user_registration(self):
        """
        Doğru veriler ile kayit işlemi
        @data : disaridan verilecek input bilgisi
        """
        data = {"username": "ayse", "password": "sifre1234"}

        response = self.client.post(self.url, data)
        self.assertEqual(201, response.status_code)

    def test_invalid_pwd(self):
        """
        Invalid pswd ile kayit
        """
        data = {"username": "ayse", "password": ""}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unique_name(self):
        """unique name test"""

        self.test_user_registration()  # create user

        data = {"username": "ayse", "password": "sifre1234"}

        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_auth_registration(self):
        """
        session ile giriş yapmis user sayfayi görememeli

        self.client.login() ile giriş saglanir
        """
        self.test_user_registration()  # register olundu
        self.client.login(username="ayse", password="sifre1234")  # giris yaoildi
        response = self.client.get(self.url)  # 403 - zaten giris yapildigi icin
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_auth_token_registration(self):
        """
        token ile giriş
        """
        self.test_user_registration()  # kul olusturuldu
        data = {"username": "ayse", "password": "sifre1234"}
        response = self.client.post(self.url_access, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # response access, refresh tokenlarini dondurur.
        token = response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        # gelen tokenı headera gönderdik
        # tekrar giriş yapmaya çalışırsak 403 almalıyız, zaten oturum açmış old. için
        response2 = self.client.get(self.url)
        self.assertEqual(403, response2.status_code)


class TestUserLogin(APITestCase):
    url_login = reverse("token_obtain_pair")

    # setUp hazır method override edilmiştir.
    # testler çalışmadan önce çalışan method, test için constructor olarak düşünülebilir.

    # tearDown hazır method override edilmiştir.
    # testler çalışmadan önce çalışan method, test için destructor olarak düşünülebilir.

    def setUp(self) -> None:  # login
        # tokena request atmak için bir üyelik olmalı
        # test çalışma sırasında ilk çalışan setUpta tokenı-logini check etmek en mantıklısı

        self.username = "ayse"
        self.password = "sifre1234"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_user_token(self):
        """
        varolan kul ile token olusturulmak istenirse 200 donmeli
        """
        data = {"username": "ayse", "password": "sifre1234"}
        response = self.client.post(self.url_access, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in json.loads(response.content))

    def test_user_invalid_data(self):
        """Invalid degerler ile giris yapilmaya calisilirsa
        401 dondurmeli"""
        data = {"username": "şlwkejrfh", "password": "sifre1234"}
        response = self.client.post(self.url_access, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_empty_data(self):
        """Bos degerler ile giris yapilmaya calisilirsa
        400 Bad Request dondurmeli"""
        data = {"username": "", "password": ""}
        response = self.client.post(self.url_access, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def tearDown(self) -> None:  # logout
        return super().tearDown()
