from django.http import HttpResponse, HttpRequest
from django.conf import settings
from tischkicker.utils import render
from django.shortcuts import redirect
from braschuene.models import Debt, User


# Create your views here.
def index(request: HttpRequest) -> HttpResponse:
    """An example view"""

    return render(
        request,
        "braschuene/index.html",
        {
            "debts": Debt.objects.order_by("-date"),
            "users": User.objects.order_by("username"),
        },
        {
            "helpText": "Everything in this dictionary is available in the javascriptContext automatically."
        },
    )


def add_debt(request: HttpRequest) -> HttpResponse:
    """Add debts"""
    receivers = request.POST.getlist("receivers")
    senders = request.POST.getlist("senders")
    amount = request.POST.get("amount")
    note = request.POST.get("note")

    debt = Debt.objects.create(amount=amount, note=note)
    debt.receivers.set(User.objects.filter(pk__in=receivers))
    debt.senders.set(User.objects.filter(pk__in=senders))
    return redirect("index")


def done(request: HttpRequest, id: int) -> HttpResponse:
    """Mark debt as done"""
    Debt.objects.filter(pk=id).update(done=True)
    return redirect("index")


def double(request: HttpRequest, id: int) -> HttpResponse:
    """Mark debt as done"""
    debt = Debt.objects.get(pk=id)
    newAmount = min(2 * debt.amount, 24)
    if debt.amount < 24:
        debt.note = f"{debt.note}\n(Verdoppelt von {debt.amount} zu {'1 Kiste' if newAmount == 24 else newAmount})".strip()
    debt.amount = newAmount
    debt.save()
    return redirect("index")
