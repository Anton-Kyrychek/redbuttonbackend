from django.urls import path

from .views import *

urlpatterns = [
    path('', button),
    path('reg_code_check/', reg_code_check),
    # path('get_buttons/', get_buttons),
]
