from unittest.mock import patch

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email="user@bodegonasusalud.com", password="testpass"):
    """Creates a simple user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = "user@bodegonasusalud.com"
        password = "testpass"
        user = sample_user()

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        email = "user@BODEGONASUSALUD.com"
        user = get_user_model().objects.create_user(email, "test123")

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_new_super_user(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            email='user@bodegonasusalud.com',
            password='password123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_categories_str(self):
        """Test the categories representation"""
        category = models.Categories.objects.create(
            user=sample_user(),
            name='Vinos'
        )

        self.assertEqual(str(category), category.name)

    def test_products_str(self):
        """Test the products representation"""
        product = models.Products.objects.create(
            user=sample_user(),
            name='Santa Ana',
            description='El vino Santa ana es un vino tinto...',
            price=15.00,
            weight="0.70",
            units='l',
            featured=False,
        )

        self.assertEqual(str(product), product.name)

    @patch('uuid.uuid4')
    def test_product_file_name_uuid(self, mock_uuid):
        """Test that the image is saved in the correct location"""
        uuid = 'test-uuid'
        mock_uuid.return_value = uuid
        file_path = models.product_image_file_path(None, 'myimage.jpg')

        exp_path = f'uploads/product/{uuid}.jpg'
        self.assertEqual(file_path, exp_path)
