import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from hw8.models import Task, SubTask
from hw8.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer


class TaskListView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        self.page_size = self.get_page_size(request)

        filters = {}
        week_day = request.query_params.get('week_day')
        if week_day:
            filters['created_at__week_day'] = week_day

        tasks = Task.objects.filter(**filters)
        results = self.paginate_queryset(tasks, request, view=self)
        serializer = TaskDetailSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)

        return self.page_size


@api_view(['GET'])
def task_one(request, id):
    try:
        task = Task.objects.get(pk=id)
        serializer = TaskDetailSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return Response(e.__str__(), status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def task_one(request, id):
    try:
        task = Task.objects.get(pk=id)
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except ObjectDoesNotExist as e:
        return (Response(e.__str__(), status=status.HTTP_404_NOT_FOUND))


@api_view(['GET'])
def task_statistic(request):
    total_tasks = Task.objects.count()
    tasks_by_status = Task.objects.values('status').annotate(count=Count('status'))
    overdue_tasks = Task.objects.filter(~Q(status__iexact="Done"), deadline__lt=datetime.datetime.today()).count()

    statistics = {
        'total_tasks': total_tasks,
        'tasks_by_status': {status['status']: status['count'] for status in tasks_by_status},
        'overdue_tasks': overdue_tasks,
    }

    return Response(statistics)


class SubTaskListCreateView(APIView, PageNumberPagination):
    page_size = 5

    def get(self, request):
        self.page_size = self.get_page_size(request)

        sort_by = request.query_params.get('sort_by', 'created_at')
        sort_order = request.query_params.get('sort_order', 'desc')
        if sort_order == 'desc':
            sort_by = f'-{sort_by}'

        filters = {}
        filter_task_name = request.query_params.get('parent_name')
        if filter_task_name:
            filters['task__title'] = filter_task_name

        filter_status = request.query_params.get('status')

        if filter_status and filter_status in list(zip(*SubTask.status.field.choices))[0]:
            filters['status'] = filter_status

        sub_tasks = SubTask.objects.filter(**filters).order_by(sort_by)
        results = self.paginate_queryset(sub_tasks, request, view=self)
        serializer = SubTaskCreateSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_page_size(self, request):
        page_size = request.query_params.get('page_size')
        if page_size and page_size.isdigit():
            return int(page_size)

        return self.page_size


class SubTaskDetailUpdateDeleteView(APIView):
    def get(self, request, pk):
        try:
            sub_task = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(sub_task)
        return Response(serializer.data)

    def patch(self, request, pk):
        try:
            sub_task = SubTask.objects.get(pk=pk)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = SubTaskCreateSerializer(sub_task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            sub_task = SubTask.objects.get(pk=id)
        except SubTask.DoesNotExist:
            return Response({'error': 'Subtask not found'}, status=status.HTTP_404_NOT_FOUND)

        sub_task.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
