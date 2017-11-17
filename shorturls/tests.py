from django.test import TestCase
from .models import Link
from django.core.urlresolvers import reverse

class ShortenerText(TestCase):
    def test_shortens(self):
        '''
        Test that urls get shorter.
        '''
        url = "http://www.example.com/"
        l = Link(url=url)
        short_url = Link.shorten(l)
        self.assertLess(len(short_url), len(url))

    def test_recover_link(self):
        '''
        Test that shortened and expanded url is the same as original.
        '''
        url = "http://www.example.com/"
        l = Link(url=url)
        short_url = Link.shorten(l)
        l.save()
        #Another user asks for the expansion of short_url
        exp_url = Link.expand(short_url)
        self.assertEqual(url, exp_url)

    def test_homepage(self):
        '''
        Tests that homepage exists and contains a form.
        '''
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertIn("form", response.context)

    def test_shortener_form(self):
        '''
        Tests that submitting a form returns a Link object.
        '''
        url = "http://example.com/"
        response = self.client.post(reverse("home"), {"url": url}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn("link", response.context)
        l = response.context["link"]
        short_url = Link.shorten(l)
        self.assertEqual(url, l.url)
        self.assertIn(short_url, response.content)