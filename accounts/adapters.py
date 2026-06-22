from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def get_login_redirect_url(self, request):
        try:
            profile = request.user.profile
            if not profile.onboarding_complete:
                next_url = request.GET.get('next', '')
                if next_url and next_url.startswith('/pago/'):
                    return next_url
                if next_url:
                    request.session['post_onboarding_next'] = next_url
                return '/onboarding/'
        except Exception:
            pass
        return super().get_login_redirect_url(request)
