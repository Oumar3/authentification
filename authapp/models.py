from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,User
from .manager import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

# Create your models here.

class CustomeUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Email and password are required. Other fields are optional.
    """
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True,unique=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    is_editor = models.BooleanField(
        _("editor status"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as editor. "
            "Unselect this instead of deleting accounts."
        ),
    )
    
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _("CustomeUser")
        verbose_name_plural = _("CustomeUsers")

    

    # def save(self, *args, **kwargs):
    #     s
    #     return super().save(*args, **kwargs)
        