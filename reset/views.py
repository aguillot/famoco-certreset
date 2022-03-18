from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.urls import reverse

from reset.forms import TokenForm
from . import mdm


class HomeView(View):
    def get(self, request, *args, **kwargs):
        form = TokenForm()
        return render(request, "home.html", {"form": form})


class DevicesView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        if token := request.GET.get("token", False):
            if not mdm.token_is_valid(token):
                return HttpResponseRedirect(reverse("home"))
            org = mdm.get_org(token)
            devices = mdm.get_devices_with_cert(token, org["id"])
            data = {
                "token": token,
                "org": org,
                "devices": devices,
            }
            return render(request, "devices.html", data)


class ResetView(View):
    def get(self, request: HttpRequest, org_id, famoco_id):
        token = request.GET.get("token")
        data = {
            "org_id": org_id,
            "famoco_id": famoco_id,
            "token": token,
            "status_code": mdm.reset_cert(token, famoco_id),
        }
        return render(request, "reset.html", data)