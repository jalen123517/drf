from rest_framework import serializers
from students.models import Student


class StudentModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Student
        fields = ["id", "name", "age", "sex","is_18"]
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4},
            "age": {"max_value": 150, "min_value": 0},
        }

    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate(self, attrs):
        name = attrs.get('name')
        age = attrs.get('age')

        if name == "alex" and age == 22:
            raise serializers.ValidationError("alex在22时的故事。。。")

        return attrs
    # 数据保存
    def create(self, validated_data):
        """接受客户端提交的新增数据"""
        print(validated_data)
        name = validated_data.get('name')
        age = validated_data.get('age')
        # sex = validated_data.get('sex')

        instance = Student.objects.create(name="zhansan", age=age)
        # instance = Student.objects.create(**validated_data)
        print("nihao")
        return instance




