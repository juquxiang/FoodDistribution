# # -*- coding: utf-8 -*-
# def jwt_response_payload_handler(token, user=None, request=None, role=None):
#     """
#         自定义jwt认证成功返回数据
#         :token 返回的jwt
#         :user 当前登录的用户信息[对象]
#         :request 当前本次客户端提交过来的数据
#         :role 角色
#     """
#     if user.first_name:
#         name = user.first_name
#     else:
#         name = user.username
#         return {
#             'authenticated': 'true',
#              'id': user.id,
#              "role": role,
#              'name': name,
#              'username': user.username,
#              'email': user.email,
#              'token': token,
#         }
# def jwt_response_payload_handler(token, user=None, request=None):
#     """
#     自定义返回认证信息
#     :param token: jwt认证token
#     :param user: 用户id
#     :param request: 请求对象
#     :return:
#     """
#     return {
#         "token": token,
#         'id': user.id,
#         'permission': user.permission
#     }
