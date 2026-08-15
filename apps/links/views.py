from __future__ import annotations
from typing import TYPE_CHECKING, cast

from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST

from .forms import LinkForm
from .services import create_short_link

if TYPE_CHECKING:
    from apps.users.models import User


def home_view(request: HttpRequest):
    form = LinkForm()
    return render(request, "home.html", {"form": form})


@require_POST
def create_short_link_view(request: HttpRequest):
    if not request.headers.get("HX-Request"):
        return redirect("home")
    form = LinkForm(request.POST)
    if form.is_valid():
        original_url = form.cleaned_data["original_url"]
        user = cast(User, request.user) if request.user.is_authenticated else None
        link = create_short_link(original_url=original_url, user=user)
        return render(request, "home.html#link_and_qr", {"link": link})
    else:
        form = LinkForm()
    return render(request, "home.html", {"form": form})
