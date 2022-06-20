import json
from unittest.mock import patch
from django.core import mail


def test_send_email_should_succeed(mailoutbox, settings) -> None:
    settings.EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
    assert len(mailoutbox) == 0
    mail.send_mail(
        subject="Test Subject",
        message="Test Message",
        from_email="teste@teste.com",
        recipient_list=["teste2@teste.com"],
        fail_silently=False,
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].subject == "Test Subject"


def test_send_email_without_arguments_should_send_empty_email(client) -> None:
    response = client.post(path="/send-email")
    response_content = json.loads(response.content)
    assert response.status_code == 200
    assert response_content["status"] == "success"
    assert response_content["info"] == "email sent successfully"
