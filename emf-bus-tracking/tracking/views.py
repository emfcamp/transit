import base64
import binascii
import hmac
import json
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from . import tasks


def index(request):
    return redirect("https://bus.emf.camp")


@csrf_exempt
def kosmos_webhook(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    if request.headers.get("Content-Type") != "application/json":
        return HttpResponse(status=415)

    kosmos_mac = request.headers.get("Kosmos-MAC")
    if not kosmos_mac:
        return HttpResponse(status=400)
    try:
        kosmos_mac = base64.b64decode(kosmos_mac)
    except binascii.Error:
        return HttpResponse(status=400)

    own_mac = hmac.digest(settings.KOSMOS_MAC_KEY.encode(), request.body, "sha256")

    if not hmac.compare_digest(kosmos_mac, own_mac):
        return HttpResponse(status=403)

    data = json.loads(request.body)

    if "type" not in data:
        return HttpResponse(status=400)

    tasks.kosmos_tasks.handle_kosmos_message.delay(data)

    return HttpResponse(status=204)
