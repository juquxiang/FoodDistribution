from datetime import datetime, timedelta

import jwt
from django.db.models import Q
from django.http import JsonResponse
# Create your views here.
from rest_framework import serializers
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet

from apps.order_manage.models import Order
from apps.user_manage.models import User
from common.const import SECRET_KEY


# 分页（局部）：自定义分页器 局部
class PageNum(PageNumberPagination):
    # 查询字符串中代表每页返回数据数量的参数名, 默认值: None
    page_size_query_param = 'page_size'
    # 查询字符串中代表页码的参数名, 有默认值: page
    # page_query_param = 'page'
    # 一页中多的结果条数
    max_page_size = 6


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        # exclude = ['id', 'password']


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(methods=['post'], detail=False, url_path='register')
    def register(self, request, *args, **kwargs):
        data = request.data.copy()
        """用户注册"""
        username = request.data.get('username')
        password = request.data.get('password')
        dormitory = request.data.get('dormitory')
        roomNumber = request.data.get('roomNumber')
        old_user = User.objects.filter(Q(username=username) | Q(dormitory=dormitory, roomNumber=roomNumber))
        if old_user:
            if User.objects.filter(username=username):
                return JsonResponse(data={'code': '400', 'msg': '该学号已注册'})
            else:
                return JsonResponse(data={'code': '400', 'msg': '该宿舍已注册'})
        else:
            user = UserSerializer(data=data)
            user.is_valid(raise_exception=True)
            user.save()
            return JsonResponse(data={'code': '201', 'msg': '注册成功'})

    @action(methods=['post'], detail=False, url_path='login')
    def login(self, request):
        data = request.data.copy()
        username = data.get('username')
        password = data.get('password')
        user = User.objects.filter(username=username).filter(password=password)
        if user:
            user = user[0]
            payload = {
                'exp': datetime.now() + timedelta(days=7),
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'dormitory': user.dormitory,
                    'roomNumber': user.roomNumber,
                    'permission': user.permission,
                }
            }
            # 生成token
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256').decode()

            response = JsonResponse(data={'code': '200', 'msg': '登录成功'})
            response.set_cookie('Authorization', token, expires=datetime.now() + timedelta(days=7))
            return response
        elif User.objects.filter(username=username):
            return JsonResponse(data={'code': '400', 'msg': '密码错误'})
        else:
            return JsonResponse(data={'code': '400', 'msg': '账号未注册'})

    @action(methods=['get'], detail=False, url_path='info')
    def get_user(self, request, *args, **kwargs):
        """ 用户详情 """
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
                return JsonResponse(payload['data'])
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    # @action(methods=['post'], detail=False, url_path='info')
    # def update_user(self, request, *args, **kwargs):
    #
    def list(self, request, *args, **kwargs):
        data = request.GET.copy()
        dormitory = data.get('dormitory', None)
        roomNumber = data.get('roomNumber', None)
        if dormitory == '':
            dormitory = '.*'
        if roomNumber == '':
            roomNumber = '.*'
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            permission = payload['data']['permission']
            if permission:
                users = User.objects.filter(dormitory__regex=dormitory).filter(roomNumber__regex=roomNumber).filter(
                    permission=0)
            else:
                return JsonResponse(data={'code': '403', 'msg': '您不是管理员。'})
            if users:
                s = UserSerializer(instance=users, many=True)
                return JsonResponse(data={'code': '200', 'data': s.data}, safe=False)
            else:
                return JsonResponse(data={'code': '404', 'msg': '用户不存在。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    def destroy(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            permission = payload['data']['permission']
            if permission:
                try:
                    instance = self.get_object()
                    serializer = self.get_serializer(instance)
                    user = User.objects.get(username=serializer.data['username'])
                    userId = user.id
                    print(userId)
                    Order.objects.filter(userId=userId).delete()
                    self.perform_destroy(instance)
                    return JsonResponse(data={'code': '200', 'msg': '删除成功。'})
                except:
                    return JsonResponse(data={'code': '404', 'msg': '用户不存在。'})
            else:
                return JsonResponse(data={'code': '403', 'msg': '您不是管理员。'})

        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
