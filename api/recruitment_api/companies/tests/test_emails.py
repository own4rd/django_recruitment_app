import json
from unittest.mock import patch
from django.core import mail
from django.test import TestCase


class EmailUnitTest(TestCase):
    def test_send_email_should_succeed(self) -> None:
        with self.settings(
            EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
        ):
            self.assertEqual(len(mail.outbox), 0)
            mail.send_mail(
                subject="Test Subject",
                message="Test Message",
                from_email="teste@teste.com",
                recipient_list=["teste2@teste.com"],
                fail_silently=False,
            )
            self.assertEqual(len(mail.outbox), 1)
            self.assertEqual(mail.outbox[0].subject, "Test Subject")

    def test_send_email_without_arguments_should_send_empty_email(self) -> None:
        # MOCK A FUNCTION into var
        with patch(
            "recruitment_api.companies.views.api_company.send_email"
        ) as mocked_send_mail_function:
            response = self.client.post(path='/send-email')
            response_content = json.loads(response.content)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response_content['status'], 'success')
            self.assertEqual(response_content['info'], 'email sent successfully')
            mocked_send_mail_function.assert_called_with(
                subject=None,
                message=None,
                from_email="test@test.com",
                recipient_list=["test2@test.com"]
            )