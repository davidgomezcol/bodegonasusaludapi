import uuid
import os
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.conf import settings

ORDER_STATUS_CHOICES = (
    ("Created", "Created"),
    ("Shipped", "Shipped"),
    ("Completed", "Completed"),
    ("Refunded", "Refunded"),
)


def product_image_file_path(_, filename):
    """Generates file path for new product image"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    return os.path.join("product/", filename)


def _generate_tracking_number():
    return get_random_string(10).upper()


class UserManager(BaseUserManager):
    """Custom UserManager Model that supports saving user with email instead of username"""

    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError("Users must have an email address.")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new SuperUser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom User Model that supports using email instead of username"""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    zip_code = models.IntegerField(default=1000)
    phone = models.CharField(max_length=20)
    id_type = models.CharField(max_length=20)
    id_number = models.IntegerField(default=1000)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "email"


class Categories(models.Model):
    """Category to be used for a product"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.name


class Products(models.Model):
    """Product to be saved with a category"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ManyToManyField("Categories")
    weight = models.CharField(max_length=50)
    units = models.CharField(max_length=50)
    featured = models.BooleanField(default=False)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    image = models.ImageField(null=True, upload_to=product_image_file_path)

    def __str__(self):  # pylint: disable=invalid-str-returned
        return self.name


class Orders(models.Model):
    """Orders that will be created with products and users"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    order_status = models.CharField(
        max_length=20, choices=ORDER_STATUS_CHOICES, default="Created"
    )
    payment_mode = models.CharField(max_length=255, null=False)
    tracking_number = models.CharField(
        max_length=150, null=True, default=_generate_tracking_number, unique=True
    )
    order_total = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )
    is_paid = models.BooleanField(default=False)
    order_date = models.DateField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    shipped_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"{self.id} - {self.tracking_number}"


class OrderItem(models.Model):
    """Order items of the Order"""

    order = models.ForeignKey(
        "Orders", related_name="order_items", on_delete=models.CASCADE
    )
    product = models.ForeignKey("Products", on_delete=models.CASCADE)
    quantity = models.IntegerField()
    item_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True
    )

    def __str__(self):
        return f"{self.order.id} - {self.order.tracking_number}"
