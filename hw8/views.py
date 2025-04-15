import datetime

from django.contrib.auth import authenticate
from django.contrib.auth.models import AnonymousUser
from django.db.models import Q, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, filters
from rest_framework.decorators import api_view, action
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from hw8.models import Task, SubTask, Category
from hw8.permissions import IsOwnerOrReadOnly
from hw8.serializers import TaskCreateSerializer, TaskDetailSerializer, SubTaskCreateSerializer, \
    CategoryCreateSerializer, RegisterSerializer, LoginSerializer


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
            tasks = data=Task.objects.filter(owner=self.request.user)
            serializer = self.get_serializer_class()(tasks, many=True)
            data = serializer.data

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


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'Пользователь успешно зарегистрирован.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            access_expiry = datetime.datetime.utcfromtimestamp(refresh.access_token['exp'])
            refresh_expiry = datetime.datetime.utcfromtimestamp(refresh['exp'])
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
            response_data = {
                'access': access_token,
                'refresh': refresh_token,
            }

            response = Response(response_data, status=status.HTTP_200_OK)
            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,
                expires=access_expiry
            )
            response.set_cookie(
                key='refresh_token',
                value=refresh,
                httponly=True,
                secure=False,
                expires=refresh_expiry
            )
            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                response = Response({"message": "Вы успешно вышли из аккаунта."}, status=status.HTTP_205_RESET_CONTENT)
                response.delete_cookie('access_token')
                response.delete_cookie('refresh_token')

                return response
            except Exception as e:
                return Response({"error": "Произошла ошибка при выходе из аккаунта."},
                                status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Refresh токен не предоставлен."}, status=status.HTTP_400_BAD_REQUEST)
