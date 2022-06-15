from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.timezone import now


class Company(models.Model):
    class CompanyStatus(models.TextChoices):
        LAYOFFS = _("Layoffs")
        HIRING_FREEZE = _("Contratação parada")
        HIRING = _("Contratando")

    name = models.CharField(_("Nome"), max_length=30, unique=True)
    status = models.CharField(
        _("Status"),
        choices=CompanyStatus.choices,
        default=CompanyStatus.HIRING,
        max_length=30,
    )
    notes = models.TextField(blank=True)
    last_update = models.DateTimeField(_("Atualização"), default=now, editable=True)
    application_link = models.URLField(max_length=100, blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
