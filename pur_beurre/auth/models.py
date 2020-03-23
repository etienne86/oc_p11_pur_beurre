from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from off_sub.models import Product

# The classes MyUserManager and MyUser are issued from django documentation:
# https://docs.djangoproject.com/en/3.0/topics/auth/customizing/#a-full-example


class MyUserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, first name and password.
        """
        if not email:
            raise ValueError('Le courriel est requis pour s\'inscrire.')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name="superuser"):
        """
        Creates and saves a superuser with the given email,
        first name and password.
        """
        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='Courriel',
        max_length=255,
        unique=True,
        error_messages={'unique': "Un compte est déjà créé avec cet email.",}
    )
    first_name = models.CharField(
        max_length=30,
        verbose_name='Prénom'
    )
    # create association table my_auth_myuser_favorites in database
    favorites = models.ManyToManyField(
        Product,
        related_name='interested_users',
        blank=True
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return f"{self.first_name} ({self.email})"

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def add_favorite(self, product):
        """
        Add a product to the list of favorites for the user.
        """
        self.favorites.add(product)

    # def is_favorite(self, product):
    #     """
    #     Returns True if the product is among the favorites for the user,
    #     False if not.
    #     """
    #     return (product in self.favorites.all())

    # def my_favorites(self):
    #     """
    #     Returns the QuerySet containing the favorites for the user.
    #     The QuerySet is empty if the user has not registered any favorite yet.
    #     """
    #     return self.favorites.all()

    def remove_favorite(self, product):
        """
        Remove a product from the list of favorites for the user.
        """
        self.favorites.remove(product)