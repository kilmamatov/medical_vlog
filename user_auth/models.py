from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.password_validation import validate_password
from django.db import models


class UserManager(BaseUserManager):
    use_in_migration = True

    def create_user(self, username, password=None):
        if not username:
            raise ValueError('user must have a username')
        user = self.model(
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    objects = UserManager()
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=30, unique=True)
    photo = models.ImageField(verbose_name='Фотография', blank=True, null=True)
    description = models.TextField(verbose_name='Описание', blank=True)
    password = models.CharField(max_length=128, validators=[validate_password])
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    @property
    def is_staff(self):
        return self.is_superuser

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        ordering = ('username',)
        verbose_name = 'Профиль'
        verbose_name_plural = 'Список профилей'

    def __str__(self):
        return self.username
