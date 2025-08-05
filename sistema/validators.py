from django.contrib.auth.password_validation import (
    UserAttributeSimilarityValidator,
    MinimumLengthValidator,
    CommonPasswordValidator,
    NumericPasswordValidator
)
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password, user=None):
        """Permite que la contraseña sea igual al username"""
        if user and password == user.username:
            pass  # Permite que la contraseña sea igual al usuario

    def get_help_text(self):
        return "Las contraseñas pueden ser iguales al nombre de usuario."

class CustomMinimumLengthValidator(MinimumLengthValidator):
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(f"La contraseña debe tener al menos {self.min_length} caracteres.", code="password_too_short")

    def get_help_text(self):
        return f"La contraseña debe tener al menos {self.min_length} caracteres."

class CustomCommonPasswordValidator(CommonPasswordValidator):
    def validate(self, password, user=None):
        common_passwords = ["123456", "password", "qwerty", "abc123"]
        if password in common_passwords:
            raise ValidationError("Esta contraseña es demasiado común. Elige una más segura.", code="password_too_common")

    def get_help_text(self):
        return "Evita usar contraseñas comunes como '123456' o 'password'."

class CustomNumericPasswordValidator(NumericPasswordValidator):
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError("La contraseña no puede contener solo números, debe contener al menos una letra o símbolo.", code="password_entirely_numeric")

    def get_help_text(self):
        return "Tu contraseña debe contener al menos una letra o símbolo."
