from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from students.models import Student
from .serializers import StudentSerializer
from .serializers import Student3Serializer
from .serializers import StudentModelSerializer
import json

# Create your views here.


class Student1View(View):
    def get(self, request, pk):

        # 获取数据库数据（拿出一条）
        student_obj = Student.objects.get(pk=pk)

        # 实例化序列化类对象
        serializer = StudentSerializer(instance=student_obj)

        print(serializer.data)

        # return HttpResponse(serializer.data)
        return JsonResponse(serializer.data)


class Student2View(View):
    def get(self, request):
        # 1. 获取数据库所有数据
        students_list = Student.objects.all()

        # 实例化序列化类对象
        serializer = StudentSerializer(instance=students_list, many=True)

        print(serializer.data)

        return JsonResponse(serializer.data, safe=False)


from .serializers import Student2Serializer

class Student3View(View):
    def post(self, request):
        # 获取用户提交的数据
        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = Student2Serializer(data=data_dict)

        print(serializer.is_valid(raise_exception=True))

        print(serializer.errors)

        print(serializer.validated_data)

        serializer.save()

        return JsonResponse(serializer.validated_data)

    def put(self, request, pk):
        student_obj = Student.objects.get(pk=pk)
        # 获取用户提交的数据
        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = Student2Serializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()  # 一定要在is_valid()之后调用

        return JsonResponse(serializer.validated_data)


class Student4View(View):
    def get(self, request):
        # 获取所有
        students_list = Student.objects.all()

        serializer = Student3Serializer(instance=students_list, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        # 新增数据
        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = Student3Serializer(data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()  # 此时调用create方法

        return JsonResponse(serializer.data)  #　序列化器序列化操作的字段（用户需要的字段）
        # return JsonResponse(serializer.validated_data)  # 反序列化通过校验的数据


class Student5View(View):
    def get(self, request, pk):
        # 获取一条数据
        student_obj = Student.objects.get(pk=pk)

        serializer = Student3Serializer(instance=student_obj)

        return JsonResponse(serializer.data)

    def put(self, request, pk):
        # 修改一条数据
        student_obj = Student.objects.get(pk=pk)

        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = Student3Serializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return JsonResponse(serializer.data)

    def delete(self, request, pk):
        # 删除一条数据

        student_obj = Student.objects.get(pk=pk)
        student_obj.delete()

        return HttpResponse("ok")


class Student6View(View):
    def get(self, request):

        students_list = Student.objects.all()

        serializer = StudentModelSerializer(instance=students_list, many=True)

        return JsonResponse(serializer.data, safe=False)

    def post(self, request):
        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = StudentModelSerializer(data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()  # 调用create方法

        return JsonResponse(serializer.data)


class Student7View(View):
    def get(self, request, pk):
        student_obj = Student.objects.get(pk=pk)

        serializer = StudentModelSerializer(instance=student_obj)

        return JsonResponse(serializer.data)

    def put(self, request, pk):
        student_obj = Student.objects.get(pk=pk)

        data_str = request.body.decode()
        data_dict = json.loads(data_str)

        serializer = StudentModelSerializer(instance=student_obj, data=data_dict)

        serializer.is_valid(raise_exception=True)

        serializer.save()  # 调用update方法

        return JsonResponse(serializer.data)

    def delete(self, request, pk):

        Student.objects.get(pk=pk).delete()
        return HttpResponse('ok')




