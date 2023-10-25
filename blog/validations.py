from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

AuthorModel = get_user_model()

#check the email is unique and password must be there and also +8 char lon
def registeration_validation(data):
    email = data['email'].strip()
    password = data['password'].strip()
    if not email or AuthorModel.objects.filter(email=email).exists():
      raise ValidationError('Error: Author with this email already exists in the system!')
    if not password or len(password) < 8:
        raise ValidationError('Error: Password length must be more than 8 characters!')
    return data


def validate_email(data):
    email = data['email'].strip()
    if not email:
      raise ValidationError('Error: an email is needed!')
    return True

def validate_password(data):
    password = data['password'].strip()
    if not password:
      raise ValidationError('Error:a password is needed!')
    return True
