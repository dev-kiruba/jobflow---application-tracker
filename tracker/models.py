from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Application(models.Model):
    STATUS_APPLIED = "applied"
    STATUS_INTERVIEWING = "interviewing"
    STATUS_OFFER = "offer"
    STATUS_REJECTED = "rejected"
    STATUS_WITHDRAWN = "withdrawn"

    STATUS_CHOICES = [
        (STATUS_APPLIED, "Applied"),
        (STATUS_INTERVIEWING, "Interviewing"),
        (STATUS_OFFER, "Offer"),
        (STATUS_REJECTED, "Rejected"),
        (STATUS_WITHDRAWN, "Withdrawn"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_APPLIED)
    date_applied = models.DateField()
    next_action_date = models.DateField(null=True, blank=True, help_text="Next interview, deadline, or follow-up date")
    job_url = models.URLField(blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_absolute_url(self):
        return reverse("application_detail", args=[self.pk])

    @property
    def status_color(self):
        """CSS class hook so the template can color-code each status badge."""
        return {
            self.STATUS_APPLIED: "badge-applied",
            self.STATUS_INTERVIEWING: "badge-interviewing",
            self.STATUS_OFFER: "badge-offer",
            self.STATUS_REJECTED: "badge-rejected",
            self.STATUS_WITHDRAWN: "badge-withdrawn",
        }.get(self.status, "")
