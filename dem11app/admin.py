
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(medicines)
admin.site.register(OtherAids)
admin.site.register(req_med)
admin.site.register(saving_request)
admin.site.register(Admin)
admin.site.register(Payments)