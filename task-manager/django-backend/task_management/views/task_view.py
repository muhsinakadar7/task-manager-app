from rest_framework import status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from task_management.models import Task
from task_management.selectors.task_selector import TaskSelector
from task_management.serializers.task_serializer import TaskSerializer
from task_management.services.assign_task_service import AssignTaskService

from task_management.services.create_task_service import CreateTaskService
from task_management.services.delete_task_service import DeleteTaskService
from task_management.services.update_task_service import UpdateTaskService


class TaskListCreateView(ListCreateAPIView):
    """
    List all tasks or create a new task.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskSelector.get_all_tasks()

    def perform_create(self, serializer):
        CreateTaskService.execute(
            self.request.user,
            serializer.validated_data,
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        task = CreateTaskService.execute(
            request.user,
            serializer.validated_data,
        )

        response_serializer = self.get_serializer(task)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED,
        )


class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update and delete a task.
    """

    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    queryset = Task.objects.all()

    def update(self, request, *args, **kwargs):
        task = UpdateTaskService.execute(
            request.user,
            kwargs["pk"],
            self.get_serializer(
                data=request.data,
                partial=True,
            ).validated_data,
        )

        serializer = self.get_serializer(task)

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        serializer = self.get_serializer(
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)

        task = UpdateTaskService.execute(
            request.user,
            kwargs["pk"],
            serializer.validated_data,
        )

        return Response(
            self.get_serializer(task).data
        )

    def destroy(self, request, *args, **kwargs):
        DeleteTaskService.execute(
            request.user,
            kwargs["pk"],
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )


class AssignTaskView(APIView):
    """
    Assign a task.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        assigned_to = request.data.get("assigned_to")

        task = TaskSelector.get_task_by_id(pk)

        user = task.project.members.get(
            user_id=assigned_to
        ).user

        task = AssignTaskService.execute(
            request.user,
            pk,
            user,
        )

        serializer = TaskSerializer(task)

        return Response(serializer.data)


class ChangeStatusView(APIView):
    """
    Change task status.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        status_value = request.data.get("status")

        task = ChangeStatusService.execute(
            request.user,
            pk,
            status_value,
        )

        serializer = TaskSerializer(task)

        return Response(serializer.data)