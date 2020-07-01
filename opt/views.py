from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated

# Create your views here.

class Demo1APIView(APIView):
    """只允许登录后的用户访问"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """个人中心"""
        return Response("个人中心")



class Demo2APIView(APIView):
    """只允许管理员访问"""
    permission_classes = [IsAdminUser]

    def get(self, request):
        """个人中心2"""
        return Response("个人中心2")


# 自定义权限
from rest_framework.permissions import BasePermission

class MyPermission(BasePermission):

    def has_permission(self, request, view):

        if request.user.username == "qiuping":
            return True
        return False


class Demo3APIView(APIView):
    permission_classes = [MyPermission]

    def get(self, request):
        """个人中心3"""
        return Response("个人中心3")


# 限流
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class Demo4APIView(APIView):
    throttle_classes = [UserRateThrottle, AnonRateThrottle]

    def get(self, request):
        """投票页面"""
        return Response("投票页面")


from rest_framework.generics import ListAPIView
from students.models import Student
from .serializers import StudentModelSerializer
from django_filters.rest_framework import DjangoFilterBackend

class Demo5APIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [DjangoFilterBackend]  # 全局配置后，这里就不用指定了。
    filter_fields = ['age', "id"]  # 声明过滤字段


from rest_framework.filters import OrderingFilter

class Demo6APIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]  # 局部配置会覆盖全局配置
    filter_fields = ['id', "sex"]
    ordering_fields = ['id', "age"]


# 分页
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

"""1. 自定义分页器，定制分页的相关配置"""
"""
# 页码分页  PageNumberPagination
前端访问形式：GET  http://127.0.0.1:8000/opt/data7/?page=4

page=1   limit 0,10
page=2   limit 10,20

# 偏移量分页  LimitOffsetPagination
前端访问形式：GET  http://127.0.0.1:8000/opt/data7/?start=4&size=3

start=0  limit 0,10
start=10 limit 10,10
start=20 limit 20,10
"""


class StandardPageNumberPagination(PageNumberPagination):
    """分页相关配置"""
    page_query_param = "page"          # 设置分页页码关键字名
    page_size = 3                      # 设置每页显示数据条数
    page_size_query_param = "size"     # 设置指定每页大小的关键字名
    max_page_size = 5                  # 设置每页显示最大值


class StandardLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2                  # 默认限制，默认值与PAGE_SIZE设置一致
    limit_query_param = "size"         # limit参数名
    offset_query_param = "start"       # offset参数名
    max_limit = 5                      # 最大limit限制



class Demo7APIView(ListAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    pagination_class = StandardPageNumberPagination
    # pagination_class = StandardLimitOffsetPagination


def python_shell(request):
    print(request)



