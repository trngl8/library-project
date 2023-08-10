import unittest
from index import app


class AppTestCase(unittest.TestCase):

    def setUp(self):
        """ Don't use this test on production. Local coverage """
        self.app = app.test_client()
        self.app.testing = True

    def test_home_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_index_route(self):
        response = self.app.get('/index')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_book_route(self):
        response = self.app.get('/books/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_book_order_route(self):
        response = self.app.get('/books/1/borrow')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_book_order_confirm_route(self):
        response = self.app.get('/order/1/confirm')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_profile_route(self):
        response = self.app.get('/profile')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_settings_route(self):
        response = self.app.get('/settings')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_logout_route(self):
        response = self.app.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')

    def test_cart_route(self):
        response = self.app.get('/cart')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'3 Books', response.data)
        self.assertEqual(response.content_type, 'text/html; charset=utf-8')
        self.assertEqual(response.mimetype, 'text/html')


if __name__ == '__main__':
    unittest.main()
