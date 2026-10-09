from .models import PageVisit


class PageVisitMiddleware:
    """Record successful public HTML page views without collecting IP addresses."""

    EXCLUDED_PREFIXES = ('/admin/', '/static/', '/media/', '/chatbot/')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if (
            request.method == 'GET'
            and response.status_code < 400
            and response.get('Content-Type', '').startswith('text/html')
            and not request.path.startswith(self.EXCLUDED_PREFIXES)
        ):
            PageVisit.objects.create(
                path=request.path[:255],
                user=request.user if request.user.is_authenticated else None,
            )
        return response
