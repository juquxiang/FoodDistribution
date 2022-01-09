import datetime

import jwt
from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework import serializers
# Create your views here.
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from apps.order_manage.models import Order
from apps.user_manage.models import User
from common.const import SECRET_KEY


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = "__all__"


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # http_method_names = ['get', 'put', 'patch', 'head', 'options', 'trace', 'delete', ]

    def create(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        data = request.data.copy()
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            permission = payload['data']['permission']
            # if permission == 1:
            #     return JsonResponse(data={'code': '403', 'msg': '管理员无法点餐。'})
            userId = payload['data']['id']
            user = User.objects.get(id=userId)
            if not user:
                return JsonResponse(data={'code': '40000'})
            data['userId'] = userId
            data['dormitory'] = payload['data']['dormitory']
            data['roomNumber'] = payload['data']['roomNumber']
            if int(data['roomNumber'][2]) % 2 == 0:
                data['area'] = 2
            else:
                data['area'] = 1
            if Order.objects.filter(userId=userId).filter(time_type=data['time_type']).filter(
                    c_time__gte=datetime.date.today()):
                return JsonResponse(data={'code': '400', 'msg': '今天本时间段您已经点过餐了。'})
            else:
                order = OrderSerializer(data=data)
                order.is_valid(raise_exception=True)
                order.save()
                return JsonResponse(data={'code': '200', 'msg': '已生成订单。'})

        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    @action(methods=['get'], detail=False, url_path='all')
    def get_all_order(self, request):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            userId = payload['data']['id']
            user = User.objects.get(id=userId)
            if not user:
                return JsonResponse(data={'code': '40000'})
            orders = Order.objects.filter(userId=userId)
            if orders:
                s = OrderSerializer(instance=orders, many=True)
                return JsonResponse(data={'code': '200', 'data': s.data}, safe=False)
            else:
                return JsonResponse(data={'code': '404', 'msg': '还没有订单。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    @action(methods=['get'], detail=False, url_path='some')
    def get_some_order(self, request):
        data = request.GET.copy()
        time_type = data.get('time_type', None)
        if time_type == '':
            time_type = '.*'
        area = data.get('area', None)
        if area == '':
            area = '.*'
        dormitory = data.get('dormitory', None)
        if dormitory == '':
            dormitory = '.*'
        status = data.get('status', None)
        if status == '':
            status = '.*'
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            permission = payload['data']['permission']
            if permission == 1:
                orders = Order.objects.filter(time_type__regex=time_type).filter(area__regex=area).filter(
                    dormitory__regex=dormitory).filter(
                    status__regex=status).order_by('roomNumber')
            else:
                userId = payload['data']['id']
                orders = Order.objects.filter(time_type__regex=time_type).filter(area__regex=area).filter(
                    dormitory__regex=dormitory).filter(
                    status__regex=status).filter(userId=userId).order_by('roomNumber')
            if orders:
                normal = 0
                muslim = 0
                for i in orders:
                    normal = i.normalFoods + normal
                    muslim = i.muslimFoods + muslim
                s = OrderSerializer(instance=orders, many=True)
                return JsonResponse(
                    data={'code': '200', 'number': {'normal': normal, 'muslim': muslim, }, 'data': s.data},
                    safe=False)
            else:
                return JsonResponse(data={'code': '404', 'msg': '还没有订单。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    def destroy(self, request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            try:
                instance = self.get_object()
                self.perform_destroy(instance)
                return JsonResponse(data={'code': '200', 'msg': '删除成功。'})
            except:
                return JsonResponse(data={'code': '404', 'msg': '订单不存在。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})

    @action(methods=['post'], detail=False, url_path='status')
    def update_status(self, request, *args, **kwargs):
        data = request.data.copy()
        print(data)
        token = request.META.get("HTTP_AUTHORIZATION")
        if token:
            try:
                payload = jwt.decode(token, SECRET_KEY)
            except:
                return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
            permission = payload['data']['permission']
            if permission == 1:
                try:
                    id = data['id']
                    status = data['status']
                    order = Order.objects.get(id=id)
                    order.status = status
                    order.save()
                    return JsonResponse(data={'code': '200', 'msg': '修改成功。'})
                except:
                    return JsonResponse(data={'code': '404', 'msg': '订单不存在。'})
            else:
                return JsonResponse(data={'code': '403', 'msg': '您不是管理员。'})
        else:
            return JsonResponse(data={'code': '401', 'msg': '无效的签名。'})
