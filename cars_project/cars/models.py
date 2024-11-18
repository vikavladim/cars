from django.core.validators import MinLengthValidator, RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


class Car(models.Model):
    make = models.CharField(max_length=50, help_text="Марка, например, 'Toyota', 'Ford'",
                            validators=[MinLengthValidator(2), RegexValidator(r'^[a-zA-Z\s]+$')])
    model = models.CharField(max_length=50, help_text="Например, 'Camry', 'Mustang'",
                             validators=[MinLengthValidator(2), RegexValidator(r'^[a-zA-Z\s]+$')])
    year = models.IntegerField(help_text="Год выпуска", validators=[
        MinValueValidator(1900),
        MaxValueValidator(timezone.now().year)
    ])
    description = models.TextField(help_text="Описание автомобиля", max_length=500)
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания записи")
    updated_at = models.DateTimeField(auto_now=True, help_text="Дата и время последнего обновления записи")
    owner = models.ForeignKey('auth.User', on_delete=models.CASCADE, help_text="Пользователь, который создал запись")


class Comment(models.Model):
    content = models.TextField(help_text="Содержание комментария", validators=[MinLengthValidator(10)])
    created_at = models.DateTimeField(auto_now_add=True, help_text="Дата и время создания комментария")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, help_text="Автомобиль, к которому относится комментарий")
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE,
                               help_text="Пользователь, который оставил комментарий")
