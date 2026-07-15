from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.utils.http import url_has_allowed_host_and_scheme


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_login_redirect_url(self, request):
        try:
            profile = request.user.profile
            if not profile.onboarding_complete:
                next_url = request.GET.get('next', '')
                plan = request.GET.get('plan', '')
                if next_url and next_url.startswith('/pago/'):
                    return next_url
                if plan in ('navegante', 'practicante'):
                    return '/planes/'
                if next_url and url_has_allowed_host_and_scheme(
                    next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
                ):
                    request.session['post_onboarding_next'] = next_url
                return '/onboarding/'
        except Exception:
            pass
        return super().get_login_redirect_url(request)
