from django.apps import AppConfig

default_app_config = 'apps.order_manage.OrderManageConfig'


class OrderManageConfig(AppConfig):
    name = 'apps.order_manage'
    verbose_name = "订单管理"
