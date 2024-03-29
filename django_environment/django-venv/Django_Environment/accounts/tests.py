from django.urls import reverse, resolve
from django.test import TestCase, SimpleTestCase
from django.test import TestCase, SimpleTestCase, Client
from accounts.models import ETF, ETF_instance
from accounts.views import SignUpView
from accounts.models import CustomUser as User
 
class RegisterUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
 
    def test_register_new_user(self):
        data = {'username': 'testuser2',
                'password1': 'testpass',
                'password2': 'testpass',
                'email': 'test2@test.com'}
        self.client.post(reverse('register'), data)
        self.assertEqual(User.objects.filter(username='testuser2').exists(), True)

class ETFModelTests(TestCase):
     """Tests for the ETF Model"""
    def setUp(self):
        """Create a new ETF for testing"""
        self.test_ETF = ETF(symbol = 'TEST', date_created = '2020-03-20')

    def test_ETF_str_method(self):
        """Test to ensure the __str__ method works as expected"""
        self.assertEqual(str(self.test_ETF), 'TEST')

    def test_ETF_absolute_url(self):
        """Test to ensure that the absolute URL method works as expected"""
        self.assertEqual(self.test_ETF.get_absolute_url(), reverse('ETF-detail', args = [str(self.test_ETF.id)]))

class ETF_instanceModelTests(TestCase):
    """Tests for the ETF_instance Model"""
    def setUp(self):
        """Create a new ETF_instance for testing"""
        self.test_ETF = ETF(symbol = 'TEST', date_created = '2020-03-20')
        self.test_ETF_instance = ETF_instance(date_created = '2020-03-20', ETF = self.test_ETF)

    def test_ETF_instance_str_method(self):
        """Test to ensure the __str__ method works as expected"""
        self.assertEqual(str(self.test_ETF_instance), 'ID: None ETF: TEST Date Created: 2020-03-20 Owned By: None')

    def test_ETF_instance_absolute_url(self):
        """Test to ensure that the absolute URL method works as expected"""
        self.assertEqual(self.test_ETF_instance.get_absolute_url(), reverse('ETF_instance_detail', args = [str(self.test_ETF_instance.id)]))

# Signup urls test
class TestUrls(SimpleTestCase):
    
    def test_signup_url_is_resolved(self):

        url = reverse('signup')
        print(resolve(url))
        # to check if the resolved url function == singupView 
        self.assertEquals(resolve(url).func.view_class, SignUpView)

