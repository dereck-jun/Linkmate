from django.test import TestCase, Client
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from .models import Bookmark
# Create your tests here.
class TestView(TestCase):
  def setUp(self):
    self.client = Client()
    self.user_trump = User.objects.create_user(username='trump', password='somepassword')
    self.user_obama = User.objects.create_user(username='obama', password='somepassword')
    
    
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
    
    self.assertEqual(Bookmark.objects.count(), 0)
    main_area = soup.find('div', id='main-area')
    self.assertIn('아직 북마크가 없습니다', main_area.text)
    
    bookmark_001 = Bookmark.objects.create(
      title="네이버",
      url='www.naver.com',
      author=self.user_trump
    )
    bookmark_002 = Bookmark.objects.create(
      title="구글",
      url='www.google.com',
      author=self.user_obama
    )
    
    self.assertEqual(Bookmark.objects.count(), 2)
    
    res = self.client.get('/bookmark/')
    soup = BeautifulSoup(res.content, 'html.parser')
    
    self.assertEqual(res.status_code, 200)
    soup = BeautifulSoup('div', id='main-area')
    
    self.assertIn(bookmark_001.title, main_area.text)
    self.assertIn(bookmark_002.title, main_area.text)
    self.assertNotIn('아직 게시물이 없습니다', main_area.text)
    
    self.assertIn(self.user_trump.username.upper(), main_area.text)
    self.assertIn(self.user_obama.username.upper(), main_area.text)
    