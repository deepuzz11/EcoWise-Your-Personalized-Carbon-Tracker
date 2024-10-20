import unittest
from app import app, db
from app.models import User

class UserModelTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser')
        db.session.add(user)
        db.session.commit()
        self.assertEqual(user.username, 'testuser')

if __name__ == '__main__':
    unittest.main()
