from django.shortcuts import render
from rest_framework.viewsets import ViewSet, GenericViewSet, ModelViewSet, ReadOnlyModelViewSet
from .serializers import StudentModelSerializer
from students.models import Student
from rest_framework.response import Response

# Create your views here.


class Student1ViewSet(ViewSet):
    def get_5(self, request):
        student5 = Student.objects.all()[:5]
        serializer = StudentModelSerializer(instance=student5, many=True)

        return Response(serializer.data)

    def get_3_girl(self, request):
        student3_girl = Student.objects.filter(sex=False)[:3]

        serializer = StudentModelSerializer(instance=student3_girl, many=True)

        return Response(serializer.data)

    def get_one(self, request, pk):
        student_obj = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student_obj)

        return Response(serializer.data)


class Student3GenericViewSet(GenericViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get_5(self, request):
        student5 = self.get_queryset()[:5]

        serializer = self.get_serializer(instance=student5, many=True)

        return Response(serializer.data)

    def get_3_girl(self, request):
        student3_girl = self.get_queryset().filter(sex=False)[:3]

        serializer = self.get_serializer(instance=student3_girl, many=True)

        return Response(serializer.data)


from rest_framework.mixins import ListModelMixin, CreateModelMixin, UpdateModelMixin, RetrieveModelMixin, DestroyModelMixin


class Student4GenericViewSet(GenericViewSet, ListModelMixin, CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class Student5ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


class Student6ReadOnlyModelViewSet(ReadOnlyModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


from rest_framework.decorators import action


class Student7ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    # methods 允许什么请求方式访问该方法（不区分大小写）
    # detail 是否有pk值，True有，反之没有，
    # @action(methods=['get', "POST"], detail=False)    # 生成URL'^student6/get_6/$'
    # def get_6(self, request):
    @action(methods=['get', "POST"], detail=True)  # 生成URL'^student6/(?P<pk>[^/.]+)/get_6/$'
    def get_6(self, request, pk):
        """自定义方法"""
        student6 = self.get_object()

        serializer = self.get_serializer(instance=student6)

        return Response(serializer.data)


from rest_framework.generics import GenericAPIView
from .serializers import StudentInfoModelSerializer


# 一个视图类调用两个序列化器类
class Student8GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()
    # serializer_class = StudentModelSerializer  # 不需要写序列化器类

    def get_serializer_class(self):
        if self.request.method == "GET":
            return StudentInfoModelSerializer
        return StudentModelSerializer

    def get(self, request):
        students_list = self.get_queryset()

        serializer = self.get_serializer(instance=students_list, many=True)

        return Response(serializer.data)

# 一个视图集中使用多个序列化器类
class Student9ModelViewSet(ModelViewSet):
    queryset = Student.objects.all()

    def get_serializer_class(self):
        print(111, self.action)
        if self.action == "list":
            return StudentInfoModelSerializer
        return StudentModelSerializer
