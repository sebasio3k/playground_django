import time
import logging
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

logger = logging.getLogger(__name__)
# BLOCKED_IPS = ['127.0.0.1']
BLOCKED_IPS = ['38.0.101.76']

EXCEPT_PATHS = ['/admin/', '/admin/login/', '/login']

class TimingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        end_time = time.time()
        duration_in_seconds = round(end_time - start_time, 3)
        response['X-Response-Time'] = str(duration_in_seconds)
        logger.info(
            f"{request.method} - {request.path} completed in {duration_in_seconds} seconds"
        )

        return response

class BlockIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        ip = request.META.get('REMOTE_ADDR')
        logger.info(f"Request from IP: {ip}")
        
        if ip in BLOCKED_IPS:
            return HttpResponseForbidden("Your IP is Forbidden.")
        
        return self.get_response(request)
    
class OnlyOfficeHoursMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        now_hour = time.localtime().tm_hour
        logger.info(f"Current hour: {now_hour}")
        
        # if 15 <= now_hour< 24:
        if True:
            return self.get_response(request)
        else:
            return HttpResponseForbidden("Office hours are between 9am and 5pm.")
        

class RequireLogginAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and not any(request.path.startswith(path) for path in EXCEPT_PATHS):
            logger.info(f"User {request.user} is not authenticated, redirecting to login page...")
            return redirect('admin:login')
        
        return self.get_response(request)
    