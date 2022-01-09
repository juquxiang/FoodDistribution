from django.db import models


# Create your models here.
class User(models.Model):
    role = (
        (0, "普通用户"),
        (1, "管理员")
    )
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=10, unique=True, verbose_name="学号")
    password = models.CharField(max_length=100, verbose_name="密码")
    dormitory = models.CharField(max_length=20, verbose_name="宿舍楼")
    roomNumber = models.CharField(max_length=20, verbose_name="房间号")
    permission = models.IntegerField(default=0, choices=role, verbose_name="权限")

    class Meta:
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

