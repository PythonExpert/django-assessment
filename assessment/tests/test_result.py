# -*- coding: utf-8 -*-
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class ResultTests(APITestCase):

    def setUp(self):
        self.bob = User.objects.create_superuser(
            username='bob', email='bob@example.com', password='top_secret')
        self.client.login(username='bob', password='top_secret')

    def test_getlist_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('assessment:api:list_results'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_getlist_authenticated(self):
        self.client.login(username='bob', password='top_secret')
        response = self.client.get(reverse('assessment:api:list_results'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
