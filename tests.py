import unittest

from app import app, TOKEN


class TestApp(unittest.TestCase):
    def setUp(self):
        self.token = TOKEN
        self.app = app.test_client()
        self.good_svg = """
        <svg width="100px" height="300px">
             <circle cx="50" cy="50" r="50" fill="red" />
        </svg>
        """
        self.bad_svg = "<svg><circle /></svg>"
        self.render_url = '/render/'
        self.render_url_with_token = '/render/?token=%s' % self.token

    def test_get_returns_405_method_not_allowed(self):
        response = self.app.get(self.render_url)
        self.assertEquals(response.status_code, 405)

    def test_post_without_token_returns_401_access_denied(self):
        response = self.app.post(self.render_url)
        self.assertEquals(response.status_code, 401)

    def test_post_without_svg_returns_400_bad_request(self):
        response = self.app.post(self.render_url_with_token)
        self.assertEquals(response.status_code, 400)

    def test_error_during_render_returns_500_error(self):
        response = self.app.post(self.render_url_with_token,
                                 data={'svg': self.bad_svg})
        self.assertEquals(response.status_code, 500)

    def test_post_with_svg_returns_png(self):
        response = self.app.post(self.render_url_with_token,
                                 data={'svg': self.good_svg})
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.mimetype, 'image/png')


if __name__ == '__main__':
    unittest.main()
