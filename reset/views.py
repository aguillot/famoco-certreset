from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView, View
from django.urls import reverse

from . import mdm


class HomeView(TemplateView):
    template_name = "home.html"


class DevicesView(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        if token := request.GET.get("token", False):
            if not mdm.token_is_valid(token):
                return HttpResponseRedirect(reverse("home"))
            org = mdm.get_org(token)
            device_filter = request.GET.get("device_filter", "")
            data = {
                "token": token,
                "org": org,
                "device_filter": device_filter,
            }
            if request.htmx:
                data["devices"] = mdm.get_devices_with_cert(
                    token, org["id"], device_filter
                )
                return render(request, "_devices_list.html", data)
            return render(request, "devices.html", data)


class ResetView(View):
    def get(self, request: HttpRequest, org_id, famoco_id):
        token = request.GET.get("token")
        device_filter = request.GET.get("device_filter")
        data = {
            "org_id": org_id,
            "famoco_id": famoco_id,
            "token": token,
            "status_code": mdm.reset_cert(token, famoco_id),
            "device_filter": device_filter,
        }
        return render(request, "reset.html", data)
