import pytest

from django.test import Client
from django.urls import reverse


@pytest.mark.django_db
def test_users_listed(sample_user, sample_admin_user):
    """Test that users are listed on users page"""
    client = Client()
    admin_user = sample_admin_user()
    client.force_login(admin_user)

    url = reverse("admin:core_user_changelist")
    res = client.get(url)

    user = sample_user()

    assert (res, user.name)
    assert (res, user.email)


@pytest.mark.django_db
def test_user_change_page(sample_user, sample_admin_user):
    """Test that the user edit page works"""
    client = Client()
    admin_user = sample_admin_user()
    client.force_login(admin_user)

    user = sample_user()

    url = reverse("admin:core_user_change", args=[user.id])
    res = client.get(url)
    assert (res.status_code, 200)


@pytest.mark.django_db
def test_create_user_page(sample_admin_user):
    """Test that create user page works"""
    client = Client()
    admin_user = sample_admin_user()
    client.force_login(admin_user)

    url = reverse("admin:core_user_add")
    res = client.get(url)

    assert (res.status_code, 200)
