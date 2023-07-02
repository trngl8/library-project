import unittest
from index import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_route(self):
        """ Don't use this test on production. Local coverage """
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Library', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
