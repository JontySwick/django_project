from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from rest_framework import serializers
from .models import *


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'categories', 'deadline']

    def validate_deadline(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Deadline не может быть в прошлом.")
        return value


class SubTaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubTask
        fields = '__all__'
        read_only_fields = ['created_at']


class TaskDetailSerializer(serializers.ModelSerializer):
    sub_tasks = SubTaskCreateSerializer(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'


class CategoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at']

    def _check_name(self, name):
        if Category.objects.filter(name=name).exists():
            raise serializers.ValidationError("Name already exists")

    def create(self, validated_data):
        name = validated_data.get("name")
        self._check_name(name)

        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        name = validated_data.get("name")
        self._check_name(name)

        instance.name = name
        instance.save()

        return instance


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(min_length=3, max_length=150)
    email = serializers.EmailField(max_length=254)
    password = serializers.CharField(write_only=True, min_length=8, validators=[validate_password])
    re_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 're_password')

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError('Пользователь с таким именем уже существует.')
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError('Пользователь с таким email уже зарегистрирован.')
        return value

    def validate(self, data):
        data = super().validate(data)
        if data['password'] != data['re_password']:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})
        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'), username=username, password=password)

            if user is None:
                raise serializers.ValidationError('Неверные учетные данные.')
            if not user.is_active:
                raise serializers.ValidationError('Аккаунт пользователя неактивен.')
            data['user'] = user
        else:
            raise serializers.ValidationError('Необходимо указать логин и пароль.')
        return data
