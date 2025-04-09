from django.utils import timezone
from rest_framework import serializers
from .models import *


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status',  'categories', 'deadline']

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
