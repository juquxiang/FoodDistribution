from django.apps import AppConfig

default_app_config = 'apps.user_manage.UserManageConfig'


class UserManageConfig(AppConfig):
    name = 'apps.user_manage'
    verbose_name = '用户管理'
