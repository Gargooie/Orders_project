from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Order(models.Model):
    id = models.AutoField(primary_key=True)  # Явно объявляем поле id(pylance подсвечивал ошибку)
    STATUS_CHOICES = [
        ('создан', 'Создан'),
        ('обрабатывается', 'Обрабатывается'),
        ('собирается', 'Собирается'),
        ('доставляется', 'Доставляется'),
        ('готов', 'Готов'),
    ]
    
    VOLUME_CHOICES = [
        ('single', 'Единичный'),
        ('multiple', 'Множественный'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    title = models.CharField(max_length=200, verbose_name='Наименование')
    volume_type = models.CharField(max_length=10, choices=VOLUME_CHOICES, verbose_name='Тип объема')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    document = models.FileField(upload_to='documents/', blank=True, null=True, verbose_name='Документ')
    quantity = models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='создан', verbose_name='Статус')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    ready_date = models.DateTimeField(blank=True, null=True, verbose_name='Дата готовности')
    
    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['-created_date']
    
    def __str__(self):
        if self.pk:  # Используем pk вместо id, подсвечивало ошибку тк django создает id сам
            return f"Заказ №{self.pk} - {self.title}"
        return f"Заказ - {self.title}"
    
    def save(self, *args, **kwargs):
        if self.status == 'готов' and not self.ready_date:
            self.ready_date = timezone.now()
        elif self.status != 'готов' and self.ready_date:
            self.ready_date = None
        super().save(*args, **kwargs)
