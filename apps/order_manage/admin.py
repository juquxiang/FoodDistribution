from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from apps.order_manage.models import Order


class OrderAdmin(ImportExportModelAdmin):
    list_per_page = 50
    # 设置在主页的显示
    list_display = ['id', 'userId', 'time_type', 'normalFoods', 'muslimFoods', 'remark', 'c_time', 'm_time', 'status',
                    'dormitory', 'roomNumber', 'area']
    # 排序
    ordering = ['id', 'userId', 'time_type', 'normalFoods', 'muslimFoods', 'remark', 'c_time', 'm_time', 'status',
                'dormitory', 'roomNumber', 'area']
    # 可点入字段
    list_display_links = list_display
    # 不可修改字段
    # readonly_fields = ['id', 'building', 'floor', 'room', 'created_time', 'updated_time', 'contact', 'delivery_code']
    # 内部显示字段
    # fields = ['id', 'building', 'floor', 'room', 'created_time', 'updated_time', 'contact', 'delivery_code']
    # 可搜索字段
    search_fields = ['time_type', 'normalFoods', 'muslimFoods', 'remark', 'c_time', 'm_time', 'status',
                     'dormitory', 'roomNumber', 'area']


admin.site.register(Order, OrderAdmin)
