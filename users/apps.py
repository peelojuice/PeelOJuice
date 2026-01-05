from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    
    def ready(self):
        """
        Initialize Firebase when Django app starts
        """
        # Import fcm_service to trigger Firebase initialization
        try:
            from . import fcm_service
            print("[INFO] FCM service module loaded")
        except Exception as e:
            print(f"[WARNING] Failed to load FCM service: {e}")
