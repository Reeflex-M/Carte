import unittest
from django.test import TestCase, RequestFactory
from .views import JoueurListView, JoueurDetailView
from django.contrib.auth.models import User

class TestJoueurListView(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='jacob', email='jacob@gmail.com', password='top_secret')
    def test_list_view(self):
        request = self.factory.get('/joueurs/')
        request.user = self.user
        response = JoueurListView.as_view()(request)
        self.assertEqual(response.status_code, 200)
    def test_detail_view(self):
        request = self.factory.get('/joueurs/1/')
        request.user = self.user
        response = JoueurDetailView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()