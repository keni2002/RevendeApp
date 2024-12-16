# middleware.py
from django.shortcuts import redirect

class RedirectAuthenticatedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Redirect is user is authenticated
        if request.user.is_authenticated and request.path in ['/accounts/login/', '/accounts/register/']:
            return redirect('dashboard')
        response = self.get_response(request)
        return response
