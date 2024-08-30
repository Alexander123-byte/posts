from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

NULLABLE = {
    'blank': True,
    'null': True
}


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    objects = CustomUserManager()

    username = None
    email = models.EmailField(unique=True, verbose_name='Почта', help_text='Укажите электронную почту')
    password = models.CharField(max_length=100, verbose_name='Пароль', help_text='Придумайте пароль')
    phone = PhoneNumberField(verbose_name='Номер телефона', help_text='Укажите номер телефона', **NULLABLE)
    date_birt = models.DateField(verbose_name='Дата рождения', help_text='Укажите дату Вашего рождения')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                        help_text='Дата и время создания аккаунта')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения',
                                        help_text='Дата и время последнего изменения аккаунта')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['id']


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments',
                               verbose_name='Автор', help_text='Выберите автора комментария')
    text = models.TextField(verbose_name='Текст комментария', help_text='Введите текст комментария')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                        help_text='Дата и время создания комментария')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения',
                                        help_text='Дата и время последнего изменения комментария')

    def __str__(self):
        return f'Комментарий от {self.author} ({self.date_created})'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-date_created']


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='Заголовок', help_text='Укажите заголовок поста')
    text = models.TextField(verbose_name='Текст поста', help_text='Укажите текст поста')
    image = models.ImageField(upload_to='posts/images/', verbose_name='Изображение', **NULLABLE,
                              help_text='Загрузите изображение (необязательно)')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts',
                               verbose_name='Автор', help_text='Укажите автора поста')
    comments = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='posts', **NULLABLE,
                                 verbose_name='Комментарий', help_text='Добавьте комментарий')
    date_created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания',
                                        help_text='Дата и время создания поста')
    date_updated = models.DateTimeField(auto_now=True, verbose_name='Дата последнего изменения',
                                        help_text='Дата и время последнего изменения поста')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-date_created']
