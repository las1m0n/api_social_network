from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from SocialNetwork.models import Post
from rest_framework.reverse import reverse as api_reverse
from rest_framework import status
from rest_framework_jwt.settings import api_settings
import clearbit
from pyhunter import PyHunter

PAYLOAD_HANDLER = api_settings.JWT_PAYLOAD_HANDLER
ENCODE_HANDLER = api_settings.JWT_ENCODE_HANDLER
clearbit.key = 'sk_36c9fca08d66e48ca7e2d9e65c36bac6'
hunter = PyHunter('e21bf8944afa614f644498fbd173379a789ee3a5')
clearbit.Person.version = '2018-11-19'
User = get_user_model()


class PostAPITest(APITestCase):
    def setUp(self):
        ver = hunter.email_verifier('bondarenko.oleg@corum.com')
        if ver["result"] == 'risky':
            user_obj = User(email='bondarenkonikita295@gmail.com')
            user_obj.set_password("password")
            person = clearbit.Person.find(email='bondarenkonikita296@gmail.com', stream=True)
            if person is not None:
                user_obj.first_name = person["name"]["givenName"]
                user_obj.last_name = person["name"]["familyName"]
            user_obj.save()
            post = Post.objects.create(
                user=user_obj,
                title='Random Title',
                content='random_content'
            )

    def test_single_user(self):
        if User.objects.first().first_name is not "":
            print("Name of person:" + User.objects.first().first_name, User.objects.first().last_name)
        user_count = User.objects.all().count()
        self.assertEqual(user_count, 1)

    def test_single_post(self):
        post_count = Post.objects.all().count()
        self.assertEqual(post_count, 1)

    def test_get_list(self):
        # test get list of posts
        data = {}
        url = api_reverse("api-social:post-create")
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_item(self):
        # test POST social network post
        data = {"title": "random random", "content": "Random Quiz"}
        url = api_reverse("api-social:post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item(self):
        # test the get list
        post = Post.objects.first()
        url = post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_item_user_jwt(self):
        post = Post.objects.first()
        # print(post.content)
        url = post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        user = User.objects.first()
        payload = PAYLOAD_HANDLER(user)
        token_response = ENCODE_HANDLER(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT' + token_response)  # jwt

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_post_item_user_jwt(self):
        user = User.objects.first()
        payload = PAYLOAD_HANDLER(user)
        token = ENCODE_HANDLER(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)
        data = {"title": "Some rando title", "content": "some more content"}
        url = api_reverse("api-social:post-create")
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_ownership(self):
        owner = User.objects.create(email='valera@mail.ru')
        blog_post = Post.objects.create(
                user=owner,
                title='New title',
                content='some_random_content'
                )

        user_obj = User.objects.first()
        self.assertNotEqual(user_obj.email, owner.email)
        payload = PAYLOAD_HANDLER(user_obj)
        token_rsp = ENCODE_HANDLER(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
        url = blog_post.get_api_url()
        data = {"title": "Some rando title", "content": "some more content"}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_login_and_update(self):
        data = {
            'email': 'bondarenkonikita295@gmail.com',
            'password': 'password'
        }
        url = api_reverse("api-login-auth")
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data.get("token")
        if token is not None:
            post = Post.objects.first()
            url = post.get_api_url()
            data = {"title": "Some rando title", "content": "some more content"}
            self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)  # Jwt
            response = self.client.put(url, data, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
