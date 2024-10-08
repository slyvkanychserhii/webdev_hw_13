from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.db.models import Count
from .models import Category, Task, SubTask
from .serializers import CategorySerializer, TaskSerializer, SubTaskSerializer
from .pagination import CustomPagination

class CategoryListCreateView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class TaskListCreateView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Фильтрация по полям status и deadline_lt:
    # http://127.0.0.1:8000/api/tasks/?status=1
    # http://127.0.0.1:8000/api/tasks/?deadline__lt=2024-09-27T00:00:00Z
    # http://127.0.0.1:8000/api/tasks/?deadline__gt=2024-09-27T00:00:00Z
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gt', 'lt'],
    }
    # Поиск по полям title и description:
    # http://127.0.0.1:8000/api/tasks/?search=task 1
    search_fields = ['title', 'description']
    # Сортировка по полю created_at:
    # http://127.0.0.1:8000/api/tasks/?ordering=created_at
    # Сортировка по полю created_at (по убыванию):
    # http://127.0.0.1:8000/api/tasks/?ordering=-created_at
    ordering_fields = ['created_at'] 
    
class TaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class TaskStatisticsView(APIView):
    def get(self, request):
        data = {}
        data['tasks'] = Task.objects.count()
        data['tasks_by_status'] = Task.objects.values('status').annotate(count=Count('*'))
        data['tasks_lte_now'] = Task.objects.filter(deadline__lt=timezone.now()).count()
        return Response(data, status=status.HTTP_200_OK)

class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # Фильтрация по полям status и deadline_lt:
    # http://127.0.0.1:8000/api/subtasks/?status=1
    # http://127.0.0.1:8000/api/subtasks/?deadline__lt=2024-09-27T00:00:00Z
    # http://127.0.0.1:8000/api/subtasks/?deadline__gt=2024-09-27T00:00:00Z
    filterset_fields = {
        'status': ['exact'],
        'deadline': ['exact', 'gt', 'lt'],
    }
    # Поиск по полям title и description:
    # http://127.0.0.1:8000/api/subtasks/?search=task 1
    search_fields = ['title', 'description']
    # Сортировка по полю created_at:
    # http://127.0.0.1:8000/api/subtasks/?ordering=created_at
    # Сортировка по полю created_at (по убыванию):
    # http://127.0.0.1:8000/api/subtasks/?ordering=-created_at
    ordering_fields = ['created_at']
    
class SubTaskRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskSerializer

