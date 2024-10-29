from rest_framework import viewsets, status # type: ignore
from rest_framework.decorators import action # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.permissions import IsAuthenticated # type: ignore
from .models import Notification
from .serializers import NotificationSerializer

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Limit notifications to those belonging to the logged-in user
        user = self.request.user
        return self.queryset.filter(user=user).order_by('-created_at')  # Order by most recent

    @action(detail=False, methods=['get'])
    def unread(self, request):
        # Fetch unread notifications only
        unread_notifications = self.get_queryset().filter(is_read=False)
        page = self.paginate_queryset(unread_notifications)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(unread_notifications, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_as_read(self, request, pk=None):
        # Mark a specific notification as read
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({'status': 'notification marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'])
    def mark_all_as_read(self, request):
        # Mark all notifications for the user as read
        notifications = self.get_queryset().filter(is_read=False)
        notifications.update(is_read=True)
        return Response({'status': 'all notifications marked as read'}, status=status.HTTP_200_OK)

    @action(detail=False, methods=['delete'])
    def delete_all(self, request):
        # Delete all notifications for the user
        notifications = self.get_queryset()
        notifications.delete()
        return Response({'status': 'all notifications deleted'}, status=status.HTTP_204_NO_CONTENT)
