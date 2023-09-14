from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Bookmark
# Create your tests here.
class TestView(TestCase):
  def setUp(self):
    self.client = Client()
    
  def navbar_test(self, soup):
    navbar = soup.nav
    self.assertIn('Bookmark', navbar.text)
    self.assertIn('My Page ', navbar.text)
    
    logo_btn = navbar.find('a', text='Do It Django')
    self.assertEqual(logo_btn.attrs['href'], '/')
    
    home_btn = navbar.find('a', text='Home')
    self.assertEqual(home_btn.attrs['href'], '/')
    
    bookmark_btn = navbar.find('a', text='Bookmark')
    self.assertEqual(bookmark_btn.attrs['href'], '/bookmark/')
    
    mypage_btn = navbar.find('a', text='My Page')
    self.assertEqual(mypage_btn.attrs['href'], '/mypage/')
    
  def test_post_list(self):
    res = self.client.get('/bookmark/')
    self.assertEqual(res.status_code, 200)
    
    soup = BeautifulSoup(res.content, 'html.parser')
    
    self.assertEqual(soup.title.text, 'Linkmate')
    
    self.navbar_test(soup)
    
  def test_post_detail(self):
    bookmark_000 = Bookmark.objects.create(
      title="네이버",
      url='www.naver.com',
    )
    self.assertEqual(bookmark_000.get_absolute_url(), '/bookmark/1/')
    res = self.client.get(bookmark_000.get_absolute_url())
    self.assertEqual(res.status_code, 200)
    soup = BeautifulSoup(res.content, 'html.parser')
    
    self.navbar_test(soup)