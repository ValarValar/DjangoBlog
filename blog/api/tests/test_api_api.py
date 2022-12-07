from django.contrib.auth.models import User
from django.db.models import Count
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory
from rest_framework.test import APITestCase

from api.serializers import UserListSerializer, UserPostsSerializer


class PostCreateApiTestCase(APITestCase):
    def test_not_authenticated_create_post(self):
        post = {
            "title": "string",
            "body": "string"
        }
        url = reverse('post_create')

        response = self.client.post(url, post)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_create_post_ok(self):
        user_creds = {
            'username': 'test_user',
            'password': '123qwer123!',
        }
        post = {
            "title": "string",
            "body": "string"
        }
        User.objects.create_user(**user_creds)
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)

        url = reverse('post_create')

        response = self.client.post(url, post)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

    def test_big_title_create_post_bad(self):
        user_creds = {
            'username': 'test_user',
            'password': '123qwer123!',
        }
        post = {
            "title": "string" * 30,
            "body": "string"
        }
        User.objects.create_user(**user_creds)
        user = User.objects.get(username='test_user')
        self.client.force_authenticate(user=user)
        url = reverse('post_create')

        response = self.client.post(url, post)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)


class UserListApiTestCase(APITestCase):
    def setUp(self) -> None:
        url = reverse('post_create')
        usernames = ["test_user0", "test_user1", "test_user2"]
        for i, username in enumerate(usernames):
            user_creds = {
                'username': username,
                'password': '123qwer123!',
            }
            post = {
                "title": "string",
                "body": "string"
            }
            User.objects.create_user(**user_creds)
            user = User.objects.get(username=username)
            self.client.force_authenticate(user=user)
            for _ in range(i):
                self.client.post(url, post)

        self.queryset = User.objects.annotate(posts_count=(Count('posts')))
        self.url = reverse('profiles_list')

    def test_user_list_ok(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        qs = self.queryset.order_by('id')
        serializer_data = UserListSerializer(qs, many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_user_list_ordered_post_count_ok(self):
        response = self.client.get(self.url, data={'ordering': '-posts_count'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        qs = self.queryset.order_by('-posts_count')
        serializer_data = UserListSerializer(qs, many=True).data
        self.assertEqual(response.data, serializer_data)

    def test_user_list_wrong_ordering_params_ok(self):
        response = self.client.get(self.url, data={'orderin': 'wrong_param'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        qs = self.queryset.order_by('id')
        serializer_data = UserListSerializer(qs, many=True).data
        self.assertEqual(response.data, serializer_data)


class UserPostsListApiTestCase(APITestCase):
    def setUp(self) -> None:
        url_post_create = reverse('post_create')
        self.username = "test_user"

        user_creds = {
            'username': self.username,
            'password': '123qwer123!',
        }
        post = {
            "title": "string",
            "body": "string"
        }

        User.objects.create_user(**user_creds)
        self.user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=self.user)
        for _ in range(3):
            self.client.post(url_post_create, post)

    def test_user_posts_ok(self):
        url = reverse('users_posts', args=[self.username])
        factory = APIRequestFactory()
        response = self.client.get(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        user = {
            'username': self.username,
            'posts': self.user.posts.all().order_by('-created')
        }

        serializer_data = UserPostsSerializer(user, context={'request': factory.get(url)}).data
        self.assertEqual(response.data, serializer_data)

    def test_not_existing_user(self):
        url = reverse('users_posts', args=['not_existing_username'])
        response = self.client.get(url)

        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)


class SubscribeApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.subscribe_to_username = 'test_user'
        user_creds = {
            'username': 'test_user',
            'password': '123qwer123!',
        }
        User.objects.create_user(**user_creds)

    def test_not_authenticated_subcribe(self):
        url = reverse('subscribe_on_user', args=[self.subscribe_to_username])

        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_non_existing_user_subscribe(self):
        self.subscribe_to_username = 'test_user'
        user_creds = {
            'username': 'test_user2',
            'password': '123qwer123!',
        }

        User.objects.create_user(**user_creds)
        user = User.objects.get(username='test_user2')
        self.client.force_authenticate(user=user)

        url = reverse('subscribe_on_user', args=['non_existing_username'])
        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_self_subscribe_bad(self):
        user_creds = {
            'username': 'test_user2',
            'password': '123qwer123!',
        }

        User.objects.create_user(**user_creds)
        user = User.objects.get(username='test_user2')
        self.client.force_authenticate(user=user)

        url = reverse('subscribe_on_user', args=['test_user2'])
        response = self.client.post(url)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)

    def test_subscribe_ok(self):
        user_creds = {
            'username': 'test_user2',
            'password': '123qwer123!',
        }

        User.objects.create_user(**user_creds)
        user = User.objects.get(username='test_user2')
        self.client.force_authenticate(user=user)

        url = reverse('subscribe_on_user', args=[self.subscribe_to_username])
        response = self.client.post(url)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data_subscribed = {
            'profile': {
                'subscriptions': [self.subscribe_to_username]
            }
        }
        self.assertEqual(response.data, expected_data_subscribed)

        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        expected_data_unsubscribed = {
            'profile': {
                'subscriptions': []
            }
        }
        self.assertEqual(response.data, expected_data_unsubscribed)


class MarkAsSeenApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.url_post_create = reverse('post_create')
        self.username = "test_user"
        user_creds = {
            'username': self.username,
            'password': '123qwer123!',
        }
        self.post = {
            "title": "test_post",
            "body": "test_body"
        }

        User.objects.create_user(**user_creds)

    def test_not_authenticated_mark(self):
        url = reverse('mark_seen', args=[5])

        response = self.client.post(url)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)

    def test_non_existing_post(self):
        url = reverse('mark_seen', args=[0])

        user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=user)

        response = self.client.post(url)
        self.assertEqual(status.HTTP_404_NOT_FOUND, response.status_code)

    def test_mark_as_seen_ok(self):
        user = User.objects.get(username=self.username)
        self.client.force_authenticate(user=user)
        response = self.client.post(self.url_post_create, self.post)

        post_id = response.data['id']
        url = reverse('mark_seen', args=[post_id])
        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        expected_data_marked = {
            "post": post_id,
            "seen": True
        }
        self.assertEqual(expected_data_marked, response.data)

        expected_data_unmarked = {
            "post": post_id,
            "seen": False
        }
        response = self.client.post(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(expected_data_unmarked, response.data)


class FeedApiTestCase(APITestCase):
    def setUp(self) -> None:
        self.users_creds = [
            {
                'username': 'test_user1',
                'password': '123qwer123!',
            },
            {
                'username': 'test_user2',
                'password': '123qwer123!',
            },
            {
                'username': 'test_user3',
                'password': '123qwer123!',
            },
        ]
        url_post_create = reverse('post_create')
        for creds in self.users_creds:
            User.objects.create_user(**creds)
            self.user = User.objects.get(username=creds['username'])
            self.client.force_authenticate(user=self.user)
            for i in range(4):
                post = {
                    "title": f"post № {i}",
                    "body": f"hi"
                }
                self.client.post(url_post_create, post)
            self.client.force_authenticate(user=None)

        self.our_username = 'our_user'
        our_user_creds = {
            'username': 'our_user',
            'password': '123qwer123!'
        }
        User.objects.create_user(**our_user_creds)
        self.user = User.objects.get(username=self.our_username)

    def test_not_authenticated_feed(self):
        feed_url = reverse('feed')
        response = self.client.get(feed_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empty_feed(self):
        feed_url = reverse('feed')
        self.client.force_authenticate(user=self.user)

        response = self.client.get(feed_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['results'], [])
        self.client.force_authenticate(user=None)

    def test_feed_pagination(self):
        self.client.force_authenticate(user=self.user)

        for creds in self.users_creds:
            username = creds['username']
            url = reverse('subscribe_on_user', args=[username])
            self.client.post(url)

        feed_url = reverse('feed')

        response = self.client.get(feed_url, data={'page': 1, 'seen': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 10)

        response = self.client.get(feed_url, data={'page': 2, 'seen': False})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

    def test_feed_filter_ok(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('subscribe_on_user', args=['test_user1'])
        self.client.post(url)

        feed_url = reverse('feed')

        response = self.client.get(feed_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)

        post = response.data['results'][0]
        post_id = post['id']
        url = reverse('mark_seen', args=[post_id])
        self.client.post(url)

        response = self.client.get(feed_url, data={'seen': False})
        self.assertEqual(len(response.data['results']), 3)

        response = self.client.get(feed_url, data={'seen': True})

        self.assertEqual(len(response.data['results']), 1)
