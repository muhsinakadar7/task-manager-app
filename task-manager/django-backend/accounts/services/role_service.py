class RoleService:
    """
    Service class for role and permission checks.
    """

    @staticmethod
    def is_staff(user):
        """
        Check whether the user is a staff member.
        """
        return user.is_staff

    @staticmethod
    def is_superuser(user):
        """
        Check whether the user is a superuser.
        """
        return user.is_superuser

    @staticmethod
    def is_active(user):
        """
        Check whether the user account is active.
        """
        return user.is_active

    @staticmethod
    def has_permission(user, permission):
        """
        Check whether the user has a specific permission.
        """
        return user.has_perm(permission)

    @staticmethod
    def belongs_to_group(user, group_name):
        """
        Check whether the user belongs to a specific group.
        """
        return user.groups.filter(name=group_name).exists()