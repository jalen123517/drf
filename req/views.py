from django.shortcuts import render, HttpResponse, redirect
from django.views import View
from rest_framework.response import Response
from students.models import Student
from .serializers import StudentModelSerializer

# Create your views here.


class Student1View(View):

    def get(self, request):
        print(111, type(request))
        print(222, request.GET)

        return HttpResponse("View ok")


from rest_framework.views import APIView
from rest_framework import status


class Student2APIView(APIView):
    def get(self, request):
        print(333, type(request))
        print(444, request.query_params)
        # print(555, request.data)

        # return HttpResponse("APIView ok")
        return Response({"name": "qiuping"}, status=status.HTTP_204_NO_CONTENT, headers={"names": "yuming"})



"""
使用APIView提供学生信息的5个API接口
GET    /req/student3/               # 获取全部数据
POST   /req/student3/               # 添加数据

GET    /req/student3/(?P<pk>\d+)    # 获取一条数据
PUT    /req/student3/(?P<pk>\d+)    # 更新一条数据
DELETE /req/student3/(?P<pk>\d+)    # 删除一条数据
"""


class Student3APIView(APIView):
    def get(self, request):
        """
        获取所有数据
        :param request: 请求对象
        :return: 响应所有数据返回
        """
        students_list = Student.objects.all()  # 作用：获取student所有数据，返回值为queryset类型（类似于列表）里面是所有学生对象

        serializer = StudentModelSerializer(instance=students_list, many=True)  # 作用：实例化序列化器类对象（因为students_list是多个对象的集合，so， 需要制定many=True， 返回值给对象

        return Response(serializer.data)

    def post(self, request):
        # 1. 获取用户提交的数据
        # data = request.data

        # serializer = StudentModelSerializer(data=data)
        serializer = StudentModelSerializer(data=request.data)  # 实例化对象

        serializer.is_valid(raise_exception=True)  # 触发数据校验

        serializer.save()  # 出发create方法保存数据（新增操作）

        return Response(serializer.data)


class Student4APIView(APIView):
    def get(self, request, pk):
        student_obj = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student_obj)

        return Response(serializer.data)

    def put(self, request, pk):
        student_obj = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student_obj, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request, pk):
        Student.objects.get(pk=pk).delete()
        ret = {"status": 1, "msg": "删除成功！"}
        return Response(ret, status=status.HTTP_204_NO_CONTENT)


from rest_framework.generics import GenericAPIView


class Student5GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        students_list = self.get_queryset()

        serializer = self.get_serializer(instance=students_list, many=True)

        return Response(serializer.data)

    def post(self, request):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


class Student6GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):

        # student_obj1 = self.get_queryset().get(pk=pk)
        student_obj = self.get_object()

        # print(1111, id(student_obj), id(student_obj1))  # get_object() 做了进一步的封装。

        serializer = self.get_serializer(instance=student_obj)

        return Response(serializer.data)

    def put(self, request, pk):
        student_obj = self.get_object()

        serializer = self.get_serializer(instance=student_obj, data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        self.get_object().delete()
        return Response("ok", status=status.HTTP_204_NO_CONTENT)


"""
使用GenericAPIView结合视图Mixin扩展类，快速实现数据接口的APIView
ListModelMixin      实现查询所有数据功能   get /req/student/
CreateModelMixin    实现添加数据的功能    post /req/student/

RetrieveModelMixin  实现查询一条数据功能  get /req/student/pk/
UpdateModelMixin    更新一条数据的功能    put /req/student/pk/
DestroyModelMixin   删除一条数据的功能    delete /req/student/pk/
"""

from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin


class Student7GenericAPIView(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request):
        return self.list(request)

    def post(self, request):
        return self.create(request)


class Student8GenericAPIView(GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self, request, pk):
        return self.retrieve(request)

    def put(self, request, pk):
        return self.update(request)

    def delete(self, request, pk):
        return self.destroy(request)


"""
DRF里面，内置了一些同时继承了GenericAPIView和Mixins扩展类的视图子类，
我们可以直接继承这些子类就可以生成对应的API接口
"""

"""
ListAPIView      获取所有数据
CreateAPIView    添加数据

RetrieveAPIView                 获取一条数据
UpdateAPIView                   更新一条数据
DestorAPIView                   删除一条数据
"""

from rest_framework.generics import ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateDestroyAPIView

from django_filters.rest_framework import DjangoFilterBackend
# class Student9GenericAPIView(ListAPIView, CreateAPIView):
class Student9GenericAPIView(ListCreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ('name','id')    #添加字段进行过滤

# class Student10GenericAPIView(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
class Student10GenericAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer



"""
视图集
上面５个接口使用了８行代码生成，但是我们可以发现有一半的代码重复了
所以，我们要把这些重复的代码进行整合，但是依靠原来的类视图，其实有２方面产生冲突的
1. 查询所有数据、添加数据是不需要声明pk的，而其他的接口需要    [路由冲突了]
2. 查询所有数据和查询一条数据，都是属于get请求                 [请求方法冲突了]
为了解决上面的２个问题，所以DRF提供了视图集来解决这个问题
"""

from rest_framework.viewsets import GenericViewSet, ModelViewSet


# class Student11GenericViewSet(GenericViewSet, ListModelMixin, CreateModelMixin, DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin):
class Student11GenericViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer




