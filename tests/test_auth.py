import os
import tempfile
import unittest

from website import create_app, db
from website.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        self.app = create_app()
        self.app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI=f"sqlite:///{self.db_path}",
            WTF_CSRF_ENABLED=False,
        )
        with self.app.app_context():
            db.drop_all()
            db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_signup_creates_and_authenticates_user(self):
        response = self.client.post('/sign-up', data={
            'email': 'person@example.com',
            'firstName': 'Ada',
            'password1': 'password123',
            'password2': 'password123',
        }, follow_redirects=False)
        self.assertEqual(response.status_code, 302)
        with self.app.app_context():
            self.assertIsNotNone(User.query.filter_by(email='person@example.com').first())

    def test_duplicate_email_does_not_create_second_user(self):
        payload = {
            'email': 'person@example.com',
            'firstName': 'Ada',
            'password1': 'password123',
            'password2': 'password123',
        }
        self.client.post('/sign-up', data=payload)
        self.client.post('/sign-up', data=payload)
        with self.app.app_context():
            self.assertEqual(User.query.filter_by(email='person@example.com').count(), 1)

    def test_mismatched_passwords_do_not_create_user(self):
        self.client.post('/sign-up', data={
            'email': 'person@example.com',
            'firstName': 'Ada',
            'password1': 'password123',
            'password2': 'different123',
        })
        with self.app.app_context():
            self.assertEqual(User.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
