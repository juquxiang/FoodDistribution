from django.db import models


# Create your models here.
class Order(models.Model):
    time_type = (
        (1, '早餐'),
        (2, '午餐'),
        (3, '晚餐')
    )
    status = (
        (1, '已下单'),
        (2, '已配送'),
    )
    area = (
        (1, '单号'),
        (2, '双号')
    )
    id = models.AutoField(primary_key=True)
    userId = models.IntegerField()
    time_type = models.IntegerField(blank=True, null=True, choices=time_type, verbose_name="时间段")
    normalFoods = models.IntegerField(blank=True, null=True, default=0, verbose_name="正常餐份数")
    muslimFoods = models.IntegerField(blank=True, null=True, default=0, verbose_name="清真餐份数")
    remark = models.CharField(blank=True, null=True, max_length=100, verbose_name="备注")
    c_time = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')
    m_time = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='最后修改时间')
    status = models.IntegerField(default=1, blank=True, null=True, choices=status, verbose_name="配送状态")
    dormitory = models.CharField(blank=True, null=True, max_length=20, verbose_name="宿舍楼")
    roomNumber = models.CharField(blank=True, null=True, max_length=40, verbose_name="房间号")
    area = models.IntegerField(blank=True, null=True, choices=area, verbose_name="单双号")

    class Meta:
        verbose_name = "订单"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.id)
