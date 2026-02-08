import json
from typing import Union

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.models import Group
from django.http import HttpRequest, HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _

from core import logger
from django_grep.components.site import ComponentViews, NotificationMixin


class NotificationView(ComponentViews, NotificationMixin):
    """
    Example view for handling notifications via different channels.
    """

    def get(self, request: HttpRequest) -> Union[HttpResponse, StreamingHttpResponse, JsonResponse]:
        """Handle notification requests."""
        import json as json_module

        # Check if client wants SSE stream
        if request.headers.get("Accept") == "text/event-stream":
            return self.send_notification_stream(request)

        # Check for specific notification request
        message = request.GET.get("message")
        level = request.GET.get("level", "info")

        if message:
            return self.send_notification(message=message, level=level, request=request)

        # Default: return notification stream
        return self.send_notification_stream(request)

    def post(self, request: HttpRequest) -> HttpResponse:
        """Send a notification."""
        try:
            data = json.loads(request.body)

            message = data.get("message")
            level = data.get("level", "info")
            title = data.get("title", "")
            user_ids = data.get("user_ids")

            if not message:
                return JsonResponse({"error": "Message is required"}, status=400)

            if user_ids:
                # Broadcast to specific users
                self.broadcast_notification(
                    message=message, level=level, title=title, user_ids=user_ids
                )
            else:
                # Send to current request
                return self.send_notification(
                    message=message, level=level, title=title, request=request
                )

            return JsonResponse({"success": True})

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)
        except Exception as e:
            logger.error(f"Error sending notification: {e}")
            return JsonResponse({"error": str(e)}, status=500)
