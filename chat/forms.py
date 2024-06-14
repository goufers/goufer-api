from django.contrib.auth.forms import UserCreationForm
from user.models import CustomUser


class SignUpForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password1','password2']