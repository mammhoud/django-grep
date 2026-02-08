from django.shortcuts import redirect
from django.urls import reverse_lazy

from .auth import *
from .notifications import *
from .translate import *
from .users import *


def profile_page(request):
    return redirect(reverse_lazy("handlers:profile"))
