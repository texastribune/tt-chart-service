import unittest

from app import app, TOKEN


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_get_returns_405_method_not_allowed(self):
        response = self.app.get('/render/')
        self.assertEquals(response.status_code, 405)

    def test_post_without_token_returns_401_access_denied(self):
        response = self.app.post('/render/')
        self.assertEquals(response.status_code, 401)

    def test_post_without_svg_returns_400_bad_request(self):
        response = self.app.post('/render/?token=%s' % TOKEN)
        self.assertEquals(response.status_code, 400)

    def test_error_during_render_returns_500_error(self):
        response = self.app.post('/render/?token=%s' % TOKEN,
                                 data={'svg': "<svg><circle /></svg>"})
        self.assertEquals(response.status_code, 500)

    def test_post_with_svg_returns_png(self):
        response = self.app.post('/render/?token=%s' % TOKEN, data={
            'svg': """
            <svg width="100px" height="300px">
                 <circle cx="50" cy="50" r="50" fill="red" />
            </svg>
            """
        })
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'image/png')


if __name__ == '__main__':
    unittest.main()