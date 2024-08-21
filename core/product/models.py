import uuid
from django.contrib.auth import get_user_model
from django.db import models
from django.core.validators import MinValueValidator

User = get_user_model()
class Category(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Banner(models.Model):
    title = models.CharField(
        'Название',
        max_length=123
    )
    description = models.CharField(
        'Описание',
        max_length=100
    )
    banner_image = models.ImageField(
        'Изображение',
        upload_to='media/banner_image/'
    )
    is_asset = models.BooleanField(
        'Активность'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = 'Баннеры'

class Size(models.Model):
    name = models.CharField(
        max_length=10,
        unique=True
    )

    def __str__(self):
        return self.name


class Cap(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )

    description = models.TextField(
        verbose_name='Описание'
    )
    logo = models.ImageField(
        upload_to='media/cap_logo/'
    )

    price = models.DecimalField(
        'Цена',
        max_digits=12,
        decimal_places=2,
        default=0.00
    )
    discount_price = models.DecimalField(
        'Новая цена',
        max_digits=12,
        decimal_places=2,
        default=0.00,
        blank=True,
        null=True
    )

    category = models.ManyToManyField(Category)

    sizes = models.ManyToManyField(Size)

    images = models.ManyToManyField('Image')

    brands = models.ManyToManyField('Brand')

    is_active = models.BooleanField(
        'Активность',
        default=True
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Кепка'
        verbose_name_plural = 'Кепки'

class Image(models.Model):
    image = models.ImageField('Изображение', upload_to='media/images/')

class Brand(models.Model):
    title = models.CharField(
        'Название',
        max_length=150
    )
    logo = models.ImageField('Изображение', upload_to='media/logos/')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бренд'
        verbose_name_plural = 'Бренды'


class Cart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT
    )
    cap = models.ForeignKey(
        Cap,
        on_delete=models.PROTECT
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='Кол-во',
        validators=[MinValueValidator(1)]
    )
    unique_code = models.CharField(unique=True, max_length=16, blank=True, null=True, help_text='Необязательно')

    address = models.CharField(
        'Адрес',
        max_length=300
    )
    created_date = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    update_date = models.DateTimeField(
        'Дата обновления',
        auto_now=True
    )
    status = models.PositiveSmallIntegerField(
        choices=(
            (1, 'Ожидает подтверждения'),
            (2, 'Подтвержден'),
            (3, 'Отказ')
        ),
        default=1
    )


    def save(self, *args, **kwargs):
        # Генерация уникального кода, если он не был установлен
        if not self.unique_code:
            self.unique_code = str(uuid.uuid4())[:16]
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Cart of {self.user} - {self.cap}'


    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзина'
