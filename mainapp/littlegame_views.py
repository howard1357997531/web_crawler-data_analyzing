from django.shortcuts import render, redirect
from .utils import *
from .models import *


def phone(request):
    return render(request, 'littlegame/phnoe.html', locals())


def lotto(request):
    return render(request, 'littlegame/lotto.html', locals())
