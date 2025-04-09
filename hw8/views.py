import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from hw8.models import Task, SubTask
from hw8.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer


@api_view(['GET', 'POST'])
def task_create_or_list(request):
    if request.method == 'POST':
        return task_create(request)
    else:
        return task_list(request)


def task_create(request):
    serializer = TaskCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def task_list(request):
    tasks = Task.objects.all()
    serializer = TaskDetailSerializer(tasks, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK, template_name='Task List')


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


class SubTaskListCreateView(APIView):
    def get(self, request):
        sub_tasks = SubTask.objects.all()
        serializer = SubTaskCreateSerializer(sub_tasks, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = SubTaskCreateSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
