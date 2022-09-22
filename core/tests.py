from django.test import TestCase

# Create your tests here.
# class TestCreate(APITestCase):  # eksik veri
#     def test_create(self):
#         sample = {"pub_date": "02.03.1995", "headline": "headline1", "content": "content1234"}
#         response = self.client.post(reverse("create"), sample)  # api.urls.py name="list"
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  # BAD REQ


# class TestList(APITestCase):  # 200
#     def test_create(self):
#         response = self.client.get(reverse("list"))  # api.urls.py name="list"
#         print(response.status_code)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)  # Ok


# class TestCommentList(APITestCase):
#     def test_comment_list(self):
#         response = self.client.get(reverse("comment_list"))
#         self.assertEqual(response.status_code, status.HTTP_200_OK)


# class TestCommentCreate(APITestCase):
#     def test_comment_create(self):
#         sample = {}
#         response = self.client.post(reverse("comment_create"), sample)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
