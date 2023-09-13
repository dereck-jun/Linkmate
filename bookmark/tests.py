from django.test import TestCase, Client
from bs4 import BeautifulSoup
from .models import Bookmark
# Create your tests here.
class TestView(TestCase):
  def setUp(self):
    self.client = Client()
    
  def test_bookmark_list(self):
    # 1. 북마크 목록 페이지를 가져온다
    res = self.client.get('/bookmark/')
    
    # 2. 정상적으로 페이지가 로드된다
    self.assertEquals(res.status_code, 200)
    
    # 3. 페이지 타이틀은 'Linkmate' 이다
    soup = BeautifulSoup(res.content, 'html.parser')
    self.assertEqual(soup.title.text, 'Linkmate')
    
    # 4. navbar가 있다
    navbar = soup.nav
    
    # 5. My page, Search 라는 문구가 navbar 안에 있다.
    self.assertIn('My Page', navbar.text)
    self.assertIn('Search', navbar.text)
    