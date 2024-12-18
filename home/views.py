from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import *


@login_required(login_url="/users/signin/")
def index(request):
    context = {
        "segment": "dashboard",
    }
    return render(request, "dashboard/index.html", context)
