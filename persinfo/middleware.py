# persinfo/middleware.py
# Redirects www.akhilkarwal.com → akhilkarwal.com (canonical non-www)
# This fixes the URL Canonicalization SEO failure.


class WwwRedirectMiddleware:
    """
    301 redirects www.akhilkarwal.com to akhilkarwal.com.
    Keeps the path, query string and fragment intact.
    Only active in production (when DEBUG=False).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        from django.conf import settings
        from django.http import HttpResponsePermanentRedirect

        host = request.get_host().lower()
        if not settings.DEBUG and host.startswith('www.'):
            # Strip 'www.' and redirect
            non_www = host[4:]
            redirect_url = '{}://{}{}'.format(
                request.scheme,
                non_www,
                request.get_full_path()
            )
            return HttpResponsePermanentRedirect(redirect_url)

        return self.get_response(request)


class RateLimitMiddleware:
    """
    Catches Ratelimited exceptions from django-ratelimit
    and returns a beautifully styled 429 Too Many Requests response.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_exception(self, request, exception):
        from django_ratelimit.exceptions import Ratelimited
        from django.shortcuts import render

        if isinstance(exception, Ratelimited):
            # Render a premium 429 error template with a 429 status code
            response = render(request, 'persinfo/429.html', status=429)
            response.status_code = 429
            return response
        return None

