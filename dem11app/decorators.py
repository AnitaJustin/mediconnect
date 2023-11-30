from django.shortcuts import redirect

from .models import Admin
def admin_loggedin(view_func):
    def wrapper_func(request, *args, **kwargs):
        if Admin.objects.filter(username=request.user).exists():
            print("admin")
            return redirect('admin_dashboard')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


