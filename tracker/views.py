import json
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ApplicationForm, RegisterForm
from .models import Application


def landing(request):
    if request.user.is_authenticated:
        return redirect("board")
    return render(request, "tracker/landing.html")


def demo(request):
    columns = [
        {"label": "Applied", "apps": [
            {"company": "Figma", "role": "Product Designer", "applied": "2 days ago"},
            {"company": "Notion", "role": "UX Designer", "next": "Tomorrow"},
            {"company": "Stripe", "role": "Product Designer", "applied": "Sep 10"},
        ]},
        {"label": "Interviewing", "apps": [
            {"company": "Linear", "role": "Product Designer", "next": "Sep 18"},
            {"company": "Vercel", "role": "Frontend Engineer", "next": "Sep 20"},
        ]},
        {"label": "Offer", "apps": [
            {"company": "Acme", "role": "Product Designer", "next": "Received"},
        ]},
        {"label": "Rejected", "apps": [
            {"company": "Ramp", "role": "Product Designer", "applied": "Sep 2"},
        ]},
        {"label": "Withdrawn", "apps": []},
    ]
    return render(request, "tracker/demo.html", {"columns": columns})


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Welcome! Your account has been created.")
            return redirect("dashboard")
    else:
        form = RegisterForm()

    return render(request, "tracker/register.html", {"form": form})


@login_required
def board(request):
    applications = Application.objects.filter(owner=request.user)

    columns = [
        {
            "key": key,
            "label": label,
            "applications": [a for a in applications if a.status == key],
        }
        for key, label in Application.STATUS_CHOICES
    ]

    return render(request, "tracker/board.html", {
        "columns": columns,
        "total": applications.count(),
        "status_choices": Application.STATUS_CHOICES,
    })


@login_required
@require_POST
def application_update_status(request, pk):
    application = get_object_or_404(Application, pk=pk, owner=request.user)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON")

    new_status = payload.get("status")
    valid_statuses = {key for key, _ in Application.STATUS_CHOICES}
    if new_status not in valid_statuses:
        return HttpResponseBadRequest("Invalid status")

    application.status = new_status
    application.save(update_fields=["status", "updated_at"])

    return JsonResponse({
        "ok": True,
        "id": application.pk,
        "status": application.status,
        "status_display": application.get_status_display(),
    })


@login_required
def dashboard(request):
    applications = Application.objects.filter(owner=request.user)

    status_counts = {
        label: applications.filter(status=key).count()
        for key, label in Application.STATUS_CHOICES
    }
    chart_data = [
        {"key": key, "label": label, "count": applications.filter(status=key).count()}
        for key, label in Application.STATUS_CHOICES
    ]

    upcoming_cutoff = date.today() + timedelta(days=14)
    upcoming = applications.filter(
        next_action_date__isnull=False,
        next_action_date__gte=date.today(),
        next_action_date__lte=upcoming_cutoff,
    ).order_by("next_action_date")

    context = {
        "total": applications.count(),
        "status_counts": status_counts,
        "chart_data": json.dumps(chart_data),
        "upcoming": upcoming,
        "recent": applications[:5],
    }
    return render(request, "tracker/dashboard.html", context)


@login_required
def application_list(request):
    applications = Application.objects.filter(owner=request.user)

    status_filter = request.GET.get("status")
    if status_filter:
        applications = applications.filter(status=status_filter)

    context = {
        "applications": applications,
        "status_choices": Application.STATUS_CHOICES,
        "active_status": status_filter or "",
    }
    return render(request, "tracker/application_list.html", context)


@login_required
def application_create(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.owner = request.user
            application.save()
            messages.success(request, f"Added {application.role} at {application.company}.")
            return redirect("application_list")
    else:
        form = ApplicationForm(initial={"date_applied": date.today()})

    return render(request, "tracker/application_form.html", {"form": form, "heading": "Add Application"})


@login_required
def application_update(request, pk):
    application = get_object_or_404(Application, pk=pk, owner=request.user)

    if request.method == "POST":
        form = ApplicationForm(request.POST, instance=application)
        if form.is_valid():
            form.save()
            messages.success(request, "Application updated.")
            return redirect("application_list")
    else:
        form = ApplicationForm(instance=application)

    return render(request, "tracker/application_form.html", {"form": form, "heading": "Edit Application"})


@login_required
def application_delete(request, pk):
    application = get_object_or_404(Application, pk=pk, owner=request.user)

    if request.method == "POST":
        application.delete()
        messages.success(request, "Application deleted.")
        return redirect("application_list")

    return render(request, "tracker/application_confirm_delete.html", {"application": application})
