from unittest.mock import patch
import html

from django.contrib.messages.storage.fallback import FallbackStorage
from django.contrib.sessions.middleware import SessionMiddleware
from django.db import DatabaseError
from django.test import RequestFactory, TestCase

from apps.accounts.views import login_view, register_view


def _attach_session_and_messages(request):
    session_middleware = SessionMiddleware(lambda req: None)
    session_middleware.process_request(request)
    request.session.save()
    setattr(request, "_messages", FallbackStorage(request))


class AuthViewDatabaseErrorTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_login_post_database_error_returns_safe_message(self):
        request = self.factory.post(
            "/accounts/login/",
            {"username": "user1", "password": "password1"},
        )
        _attach_session_and_messages(request)

        with patch("apps.accounts.views.authenticate", side_effect=DatabaseError("db down")):
            response = login_view(request)

        content = html.unescape(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "We're having trouble signing you in right now. Please try again shortly.",
            content,
        )

    def test_register_post_uniqueness_check_database_error_returns_safe_message(self):
        request = self.factory.post(
            "/accounts/register/",
            {
                "username": "user1",
                "email": "user1@example.com",
                "password": "password123",
                "confirm_password": "password123",
            },
        )
        _attach_session_and_messages(request)

        with patch("apps.accounts.views.User.objects.filter", side_effect=DatabaseError("db down")):
            response = register_view(request)

        content = html.unescape(response.content.decode("utf-8"))
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            "We're unable to process registration right now. Please try again shortly.",
            content,
        )
