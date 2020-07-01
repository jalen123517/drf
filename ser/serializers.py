from rest_framework import serializers
from students.models import Student


# 序列化器类，直接或者间接的继承（serializers.Serializer）
class StudentSerializer(serializers.Serializer):
    # 声明序列化器
    # 序列化阶段
    # 1. 字段声明[ 要转换的字段，当然，如果写了第二部分代码，有时候也可以不用写字段声明 ]
    id = serializers.IntegerField()
    name = serializers.CharField()
    sex = serializers.BooleanField()
    age = serializers.IntegerField()
    class_null = serializers.CharField()
    description = serializers.CharField()

    # 2. 可选[ 如果序列化器继承的是ModelSerializer，则需要声明对应的模型和字段, ModelSerializer是Serializer的子类 ]

    # 反序列化阶段
    # 3. 可选[ 用于对客户端提交的数据进行验证 ]

    # 4. 可选[ 用于把通过验证的数据进行数据库操作，保存到数据库 ]


"""
  在drf中，对于客户端提供的数据，往往需要验证数据的有效性，这部分代码是写在序列化器中的。
  在序列化器中，已经提供三个地方给我们针对客户端提交的数据进行验证。
  1. 内置选项，字段声明的小圆括号中，以选项存在作为验证提交
  2. 自定义方法，在序列化器中作为对象方法来提供验证[ 这部分验证的方法，必须以"validate_<字段>" 或者 "validate" 作为方法名 ]
  3. 自定义函数，在序列化器外部，提前声明一个验证代码，然后在字段声明的小圆括号中，通过 "validators=[验证函数１,验证函数２...]"
"""


def check_user(data):
    if data == "yuming1":
        raise serializers.ValidationError("找的就是你，盯你很久了。")
    return data


def check_user2(data):
    if data == "yuming2":
        raise serializers.ValidationError("2找的就是你，盯你很久了。")
    return data


class Student2Serializer(serializers.Serializer):
    # 字段声明
    name = serializers.CharField(max_length=10, min_length=4, validators=[check_user, check_user2])
    sex = serializers.BooleanField(required=True)
    age = serializers.IntegerField(max_value=150, min_value=0)

    # 单个字段校验
    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    def validate_age(self, data):
        if data < 18:
            raise serializers.ValidationError("年龄不能小于18岁，你未成年！")
        return data

    # 多个字段统一校验
    def validate(self, attrs):
        # print(111, attrs)
        name = attrs.get('name')
        age = attrs.get('age')

        if name == 'qiuping' and age == 19:
            raise serializers.ValidationError("臭不要脸，明明38.")
        return attrs

    # 数据保存
    def create(self, validated_data):
        """接受客户端提交的新增数据"""
        print(validated_data)
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')

        # instance = Student.objects.create(name=name, age=age, sex=sex)
        instance = Student.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中对于验证完成的数据进行保存更新"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')

        instance.name = name
        instance.age = age
        instance.sex = sex

        instance.save()
        return instance


class Student3Serializer(serializers.Serializer):
    # 合并使用
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=10, min_length=4, validators=[check_user])
    sex = serializers.BooleanField(required=True)
    age = serializers.IntegerField(max_value=150, min_value=0)
    class_null = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    # 单个字段校验
    def validate_name(self, data):
        if data == "root":
            raise serializers.ValidationError("用户名不能为root！")
        return data

    # 数据保存
    def create(self, validated_data):
        """接受客户端提交的新增数据"""
        print(validated_data)
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')

        instance = Student.objects.create(name=name, age=age, sex=sex)
        instance = Student.objects.create(**validated_data)

        return instance

    def update(self, instance, validated_data):
        """用于在反序列化中对于验证完成的数据进行保存更新"""
        name = validated_data.get('name')
        age = validated_data.get('age')
        sex = validated_data.get('sex')

        instance.name = name
        instance.age = age
        instance.sex = sex

        instance.save()
        return instance


# 模型类序列化器类


class StudentModelSerializer(serializers.ModelSerializer):
    # 1. 声明字段
    # name = serializers.CharField(max_length=10, min_length=4, validators=[check_user])

    # 2. modelSerializer
    class Meta:
        model = Student
        fields = ["id",'sex',"age","is_18","name"]  # is_18 为自定制字段，需要在models里自定义方法。
        extra_kwargs = {
            "name": {"max_length": 10, "min_length": 4, "validators": [check_user]},
            # 等同与name = serializers.CharField(max_length=10, min_length=4, validators=[check_user])
            # "age": {"max_value": 150, "min_value": 0},
            # "name":{"read_only":True},
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
