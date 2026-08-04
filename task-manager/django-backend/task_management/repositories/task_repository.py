from django.db import transaction

from task_management.models import Task


class TaskRepository:
    """
    Repository responsible for database write operations
    related to Task.
    """

    @staticmethod
    @transaction.atomic
    def create_task(**validated_data):
        """
        Create a new task.
        """
        return Task.objects.create(**validated_data)

    @staticmethod
    @transaction.atomic
    def update_task(task, **validated_data):
        """
        Update an existing task.
        """
        for field, value in validated_data.items():
            setattr(task, field, value)

        task.save()

        return task

    @staticmethod
    @transaction.atomic
    def assign_task(task, user):
        """
        Assign a task to a user.
        """
        task.assigned_to = user
        task.save(update_fields=["assigned_to", "updated_at"])

        return task

    @staticmethod
    @transaction.atomic
    def change_status(task, status):
        """
        Change task status.
        """
        task.status = status
        task.save(update_fields=["status", "updated_at"])

        return task

    @staticmethod
    @transaction.atomic
    def delete_task(task):
        """
        Delete a task.
        """
        task.delete()