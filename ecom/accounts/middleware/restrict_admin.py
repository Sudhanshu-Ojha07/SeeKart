from django.http import HttpResponseForbidden
from django.contrib.auth.models import User
from django.contrib.sessions.backends.db import SessionStore
from django.conf import settings
from django.utils.deprecation import MiddlewareMixin





class RestrictAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        allowed_ips = ['127.0.0.1']  # List of allowed IPs
        if request.path.startswith('/admin/') and request.META.get('REMOTE_ADDR') not in allowed_ips:
            return HttpResponseForbidden('<h1>403 Forbidden</h1>')
        return self.get_response(request)

#-----------------------------------------------------------------------------------------------------------------------

# from django.contrib.sessions.backends.db import SessionStore

# class SeparateSessionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Identify whether the request is for the admin panel
#         is_admin_request = request.path.startswith('/admin/')

#         # Store the current session key for admin and site separately
#         admin_session_key = request.session.get('admin_session_key')
#         site_session_key = request.session.get('site_session_key')

#         if is_admin_request:
#             if site_session_key and request.session.session_key != admin_session_key:
#                 # Save the site session key before switching to admin session
#                 request.session['site_session_key'] = request.session.session_key
#                 # Restore the admin session if it exists
#                 if admin_session_key:
#                     request.session = SessionStore(session_key=admin_session_key)
#                 else:
#                     # Start a new admin session
#                     request.session.flush()
#                     request.session['admin_session_key'] = request.session.session_key
#         else:
#             if admin_session_key and request.session.session_key != site_session_key:
#                 # Save the admin session key before switching to site session
#                 request.session['admin_session_key'] = request.session.session_key
#                 # Restore the site session if it exists
#                 if site_session_key:
#                     request.session = SessionStore(session_key=site_session_key)
#                 else:
#                     # Start a new site session
#                     request.session.flush()
#                     request.session['site_session_key'] = request.session.session_key

#         response = self.get_response(request)
#         return response
        #----------------------------------------------Or-------------------------------------------


# class AdminSiteSessionMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Check if the request is for the admin panel
#         if request.path.startswith('/admin/'):
#             # Use the admin session cookie name
#             request.session.set_cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
#         else:
#             # Use the main site session cookie name
#             request.session.set_cookie_name = settings.SESSION_COOKIE_NAME

#         response = self.get_response(request)
#         return response
#------------------------------------Or-----------------------------------------------------------------------------

# class AdminSiteSessionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         # Check if the request is for the admin panel
#         if request.path.startswith('/admin/'):
#             # Use the admin session cookie name
#             request.session_cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
#         else:
#             # Use the main site session cookie name
#             request.session_cookie_name = settings.SESSION_COOKIE_NAME

#     def process_response(self, request, response):
#         if hasattr(request, 'session_cookie_name'):
#             response.set_cookie(
#                 request.session_cookie_name,
#                 request.session.session_key,
#                 httponly=True,
#                 secure=settings.SESSION_COOKIE_SECURE,
#                 samesite=settings.SESSION_COOKIE_SAMESITE,
#             )
#         return response


#Troubleshooting part (Optional)    
# import logging

# logger = logging.getLogger(__name__)

# class AdminSiteSessionMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         if request.path.startswith('/admin/'):
#             request.session_cookie_name = settings.ADMIN_SESSION_COOKIE_NAME
#             logger.debug("Admin panel session cookie set")
#         else:
#             request.session_cookie_name = settings.SESSION_COOKIE_NAME
#             logger.debug("Main site session cookie set")
