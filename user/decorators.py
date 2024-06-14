from functools import wraps
from django.http import JsonResponse

def phone_verification_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({'detail': 'Authentication required.'}, status=401)
        if not hasattr(request.user, 'phone_verified') or not request.user.phone_verified:
            return JsonResponse({'detail': 'Phone verification required.'}, status=403)
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view

def phone_unverified(f):
    @wraps(f)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and hasattr(request.user, 'phone_verified') and not request.user.phone_verified:
            return f(request, *args, **kwargs)
        return JsonResponse({'detail': 'Phone verification already completed.'}, status=403)
    return _wrapped_view
