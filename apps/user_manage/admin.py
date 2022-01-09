from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin

from apps.user_manage.models import User


class UserAdmin(ImportExportModelAdmin):
    list_per_page = 50
    # 设置在主页的显示
    list_display = ['id', 'username', 'password', 'dormitory', 'roomNumber', 'permission']
    # 排序
    ordering = ['id', 'username', 'password', 'dormitory', 'roomNumber', 'permission']
    # 可点入字段
    list_display_links = list_display
    # 不可修改字段
    # readonly_fields = ['id', 'building', 'floor', 'room', 'created_time', 'updated_time', 'contact', 'delivery_code']
    # 内部显示字段
    # fields = ['id', 'building', 'floor', 'room', 'created_time', 'updated_time', 'contact', 'delivery_code']
    # 可搜索字段
    search_fields = ['username', 'dormitory', 'roomNumber', 'permission']


admin.site.register(User, UserAdmin)
admin.AdminSite.site_header = '疫情防控用餐管理系统'
admin.AdminSite.site_title = '疫情防控用餐管理系统'
