from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from .models import ArtProduct


class HomePageTests(TestCase):
    def test_home_page_opens(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'HomePage.html')


class ProductModelTests(TestCase):
    def test_product_creation(self):
        product = ArtProduct.objects.create(
            name='Sunset',
            price=100,
            copies=5,
            paint_type='Oils',
            material='Canvas',
            genre='Landscape'
        )

        self.assertEqual(product.name, 'Sunset')
        self.assertEqual(product.price, 100)
        self.assertEqual(product.copies, 5)


class AuthTests(TestCase):
    def test_login_page_opens(self):
        response = self.client.get(reverse('login'))

        self.assertEqual(response.status_code, 200)

    def test_user_can_login(self):
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

        logged_in = self.client.login(
            username='testuser',
            password='testpass123'
        )

        self.assertTrue(logged_in)

class ProductPageTests(TestCase):
    def setUp(self):
        self.product = ArtProduct.objects.create(
            name='Ocean',
            price=200,
            copies=3,
            paint_type='Acrylic',
            material='Canvas',
            genre='Landscape'
        )

    def test_product_details_page_opens(self):
        response = self.client.get(
            reverse('product_details', args=[self.product.id])
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Ocean')