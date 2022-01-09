# # coding:UTF-8
# # =================================================================
# # @ Author : 琚翔
# # @ Desc : 权限相关类
# # @ Date : 2021-12-28
# # @ Remark :
# # ==================================================================
#
# from rest_framework import permissions
#
#
# # TODO 下面的函数对权限验证不完全，后面有时间会修复
# class IsUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # 注册用户时候通过
#         if request.method == 'POST':
#             return True
#         user = request.user
#         # 验证用户是否被锁定
#         if not user.is_active:
#             return False
#         # 超级管理员
#         if user.is_superuser:
#             return True
#         try:
#             groups = user.groups.all()
#             for group in groups:
#                 # 普通管理员和队伍本身，放行
#                 if group.name == 'admin' or group.name == 'team':
#                     return True
#             else:
#                 return False
#         except:
#             return False
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if user.is_superuser:
#             return True
#         try:
#             groups = user.groups.all()
#             for group in groups:
#                 # 普通管理员放行
#                 if group.name == 'admin':
#                     return True
#         except:
#             return False
#         # 队伍本身，放行
#         if request.user == obj.user:
#             return True
#         else:
#             return False
#
#
# class IsTeamForMember(IsTeam):
#
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if user.is_superuser:
#             return True
#         try:
#             groups = user.groups.all()
#             for group in groups:
#                 # 普通管理员放行
#                 if group.name == 'admin':
#                     return True
#         except:
#             return False
#         # 队伍本身，放行
#         if request.user == obj.team.user:
#             return True
#         else:
#             return False
#
#
# class IsJudger(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # 这里验证一下是否是judger
#         user = request.user
#         # 验证用户是否被锁定
#         if not user.is_active:
#             return False
#         if user.is_superuser:
#             return True
#         try:
#             groups = user.groups.all()
#             for group in groups:
#                 if group.name == 'judger':
#                     return True
#             else:
#                 return False
#         except:
#             return False
#
#
# class IsCommonAdmin(permissions.BasePermission):
#     def has_permission(self, request, view):
#         # 如果是get 请求，允许通过
#         if request.method in permissions.SAFE_METHODS:
#             return True
#         user = request.user
#         # 验证用户是否被锁定
#         if not user.is_active:
#             return False
#         if user.is_superuser:
#             return True
#         try:
#             groups = user.groups.all()
#             for group in groups:
#                 if group.name == 'admin':
#                     return True
#             else:
#                 return False
#         except:
#             return False
