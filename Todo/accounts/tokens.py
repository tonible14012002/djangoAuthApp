from turtle import setx
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six  #for convert between python version

class SignUpTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.is_active)
        )

password_reset_token = PasswordResetTokenGenerator()

account_activation_token = SignUpTokenGenerator()