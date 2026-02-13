import time
import logging

logger = logging.getLogger(__name__)

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
            f"Response time: {duration_in_seconds}s | path={request.path}"
        )

        return response
