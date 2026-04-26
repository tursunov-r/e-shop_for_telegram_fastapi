from abc import ABC, abstractmethod


class EmailService(ABC):
    @abstractmethod
    def send_email(self, user_email: str, message: dict):
        pass


class SMSService(ABC):
    @abstractmethod
    def send_sms(self, phone_number: str, message: dict):
        pass


class PushNotificationService(ABC):
    @abstractmethod
    def send_push_notification(self, user_id: str, message: dict):
        pass


class NotificationService(EmailService, SMSService, PushNotificationService):
    def send_email(self, user_email: str, message: str):
        return f"Hello {user_email}!\n\n{message}"

    def send_sms(self, phone_number: str, message: str):
        return f"Hello {phone_number}!\n\n{message}"

    def send_push_notification(self, user_id: str, message: str):
        return f"Hello {user_id}!\n\n{message}"
