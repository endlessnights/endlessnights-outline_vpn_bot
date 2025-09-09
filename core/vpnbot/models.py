from django.db import models


class Post(models.Model):
    name = models.CharField(verbose_name='Заголовок', max_length=200)
    POST_CHOICES = [
        ('warning', 'Warning'),
        ('update', 'Update coming'),
        ('advert', 'Реклама'),
        ('post', 'Запись'),
    ]
    post_type = models.CharField(
        verbose_name='Тип записи',
        max_length=8,
        choices=POST_CHOICES,
        default='post',
    )
    text = models.TextField(verbose_name='Текст записи', max_length=4000, blank=True, null=True)
    image = models.ImageField(verbose_name='Изображение', upload_to='post_images/', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Accounts(models.Model):
    tgid = models.CharField(verbose_name='ID пользователя', max_length=48, null=True, unique=True, blank=True)
    tglogin = models.CharField(verbose_name='TG Username', blank=True, max_length=100, null=True)
    tgname = models.CharField(verbose_name='Имя', blank=True, max_length=100)
    regdate = models.DateTimeField(verbose_name='Дата регистрации', null=True, auto_now_add=True)
    lastdate = models.DateTimeField(verbose_name='Последнее использование', null=True, blank=True)
    CLASS_CHOICES = [
        ('free', 'Personal'),
        ('paid1', 'Plus'),
        ('paid2', 'Pro'),
        ('paid3', 'Premium'),
    ]
    rateclass = models.CharField(
        verbose_name='Тариф',
        max_length=6,
        choices=CLASS_CHOICES,
        default='free',
    )
    userlogin = models.CharField(verbose_name='user username', max_length=100, blank=True, null=True)
    username = models.CharField(verbose_name='user name', max_length=200, blank=True, null=True)
    vpn_key_id = models.CharField(verbose_name='Key ID', max_length=20, blank=True, null=True)
    vpn_key_name = models.CharField(verbose_name='Key Name', max_length=200, blank=True, null=True)
    vpn_key_password = models.CharField(verbose_name='Key password', max_length=200, blank=True, null=True)
    vpn_key_port = models.CharField(verbose_name='Key port', max_length=5, blank=True, null=True)
    vpn_access_url = models.CharField(verbose_name='Access url', max_length=250, blank=True, null=True)
    vpn_id_almaty = models.CharField(verbose_name='Key ID_almaty', max_length=20, blank=True, null=True)
    vpn_name_almaty = models.CharField(verbose_name='Key Name_almaty', max_length=200, blank=True, null=True)
    vpn_password_almaty = models.CharField(verbose_name='Key password_almaty', max_length=200, blank=True, null=True)
    vpn_port_almaty = models.CharField(verbose_name='Key port_almaty', max_length=5, blank=True, null=True)
    vpn_url_almaty = models.CharField(verbose_name='Access url_almaty', max_length=250, blank=True, null=True)
    vpn_id_spb = models.CharField(verbose_name='Key ID_spb', max_length=20, blank=True, null=True)
    vpn_name_spb = models.CharField(verbose_name='Key Name_spb', max_length=200, blank=True, null=True)
    vpn_password_spb = models.CharField(verbose_name='Key password_spb', max_length=200, blank=True, null=True)
    vpn_port_spb = models.CharField(verbose_name='Key port_spb', max_length=5, blank=True, null=True)
    vpn_url_spb = models.CharField(verbose_name='Access url_spb', max_length=250, blank=True, null=True)
    vpn_id_ny = models.CharField(verbose_name='Key ID_ny', max_length=20, blank=True, null=True)
    vpn_name_ny = models.CharField(verbose_name='Key Name_ny', max_length=200, blank=True, null=True)
    vpn_password_ny = models.CharField(verbose_name='Key password_ny', max_length=200, blank=True, null=True)
    vpn_port_ny = models.CharField(verbose_name='Key port_ny', max_length=5, blank=True, null=True)
    vpn_url_ny = models.CharField(verbose_name='Access url_ny', max_length=250, blank=True, null=True)
    has_access = models.BooleanField(verbose_name='Has access', default=False)

    def __str__(self):
        return str(self.tgid)

    def publish(self):
        self.save()

    class Meta:
        verbose_name = 'VPN Account'
        verbose_name_plural = 'VPN Accounts'
