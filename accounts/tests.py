from django.contrib.auth import get_user_model
from django.test import TestCase

from config.ai_client import user_intent_context

User = get_user_model()


class UserIntentContextTests(TestCase):
    """Regresión del typo user.userprofile → user.profile (fix 0.1).

    El related_name real del OneToOne es 'profile' (accounts/models.py). Antes
    del fix, user_intent_context lanzaba AttributeError silenciado por el
    except → devolvía '' siempre, anulando la personalización del onboarding.
    """

    def test_priorities_llegan_al_contexto(self):
        user = User.objects.create_user(email='p@test.cl', password='x')
        user.profile.onboarding_priorities = ['propio', 'familia']
        user.profile.save()

        ctx = user_intent_context(user)

        self.assertNotEqual(ctx, '')
        self.assertIn('desarrollo personal propio', ctx)
        self.assertIn('desarrollo de su familia', ctx)

    def test_sin_prioridades_devuelve_vacio(self):
        user = User.objects.create_user(email='v@test.cl', password='x')
        self.assertEqual(user_intent_context(user), '')
