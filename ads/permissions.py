from django.http import Http404
from rest_framework.permissions import BasePermission

from ads.models import Ad, Selection
from users.models import User


class SelectionUpdatePermission(BasePermission):
    message = "No permission"

    def has_permission(self, request, view):
        try:
            entity = Selection.objects.get(pk=view.kwargs['pk'])
        except Selection.DoesNotExist:
            raise Http404

        if entity.user_id == request.user.id:
            return True

        return False


class AdUpdatePermission(BasePermission):
    message = "No permission"

    def has_permission(self, request, view):
        if request.user in [User.MODERATOR, User.ADMIN] :
            return True
        try:
            entity = Ad.objects.get(pk=view.kwargs['pk'])
        except Ad.DoesNotExist:
            raise Http404

        if entity.user_id == request.user.id:
            return True

        return False