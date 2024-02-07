from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model

from core import models


@pytest.mark.django_db
def test_create_user_with_email_successful(sample_user: get_user_model):
    """Test creating a new user with an email is successful"""
    email = "user@bodegonasusalud.com"
    password = "password123"

    user = sample_user(email=email, password=password)

    assert user.email == email
    assert user.check_password(password)


@pytest.mark.django_db
def test_new_user_email_normalized(sample_user: get_user_model):
    """Test the email for a new user is normalized"""
    email = "user@BODEGONASUSALUD.com"
    user = sample_user(email=email)

    assert user.email == email.lower()


@pytest.mark.django_db
def test_new_user_invalid_email(sample_user: get_user_model):
    """Test creating user with no email raises error"""
    with pytest.raises(ValueError):
        sample_user(email=None, password="test_pass")


@pytest.mark.django_db
def test_create_new_super_user(sample_admin_user: get_user_model):
    """Test creating a new superuser"""
    user = sample_admin_user()

    assert user.is_superuser
    assert user.is_staff


@pytest.mark.django_db
def test_categories_str(sample_user, sample_category):
    """Test the categories representation"""
    user = sample_user()
    category = sample_category(user=user)

    assert str(category) == category.name


@pytest.mark.django_db
def test_products_str(sample_user, sample_product, sample_category):
    """Test the products representation"""
    user = sample_user()
    sample_category(user=user)
    product = sample_product(user=user)

    assert str(product) == product.name


@pytest.mark.django_db
@patch("uuid.uuid4")
def test_product_file_name_uuid(mock_uuid):
    """Test that the image is saved in the correct location"""
    uuid = "test-uuid"
    mock_uuid.return_value = uuid
    file_path = models.product_image_file_path("", "myimage.jpg")

    exp_path = f"product/{uuid}.jpg"
    assert file_path == exp_path
