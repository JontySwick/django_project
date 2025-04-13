import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from hw8.models import Task, SubTask, Category
from hw8.permissions import IsOwnerOrReadOnly
from hw8.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer, \
    CategoryCreateSerializer


class TaskListView(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Task.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return TaskCreateSerializer

        return TaskDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=False, methods=['get'])
    def my(self, request):
        data = {}
        if type(self.request.user) is not AnonymousUser:
            data = Task.objects.filter(owner=self.request.user)

        return Response(data)

    @action(detail=False, methods=['get'])
    def statistic(self, request):
        total_tasks = Task.objects.count()
        tasks_by_status = Task.objects.values('status').annotate(count=Count('status'))
        overdue_tasks = Task.objects.filter(~Q(status__iexact="Done"), deadline__lt=datetime.datetime.today()).count()

        statistics = {
            'total_tasks': total_tasks,
            'tasks_by_status': {status['status']: status['count'] for status in tasks_by_status},
            'overdue_tasks': overdue_tasks,
        }

        return Response(statistics)


class SubTaskListCreateView(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer


class CategoryViewSet(ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    @action(detail=False, methods=['get'])
    def count_tasks(self, request):
        data = Category.objects.annotate(task_count=Count('task')).values('id', 'name', 'task_count')

        return Response(data)
