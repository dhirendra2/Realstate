from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save, post_delete
from django.core.validators import RegexValidator
from django.contrib.auth.validators import UnicodeUsernameValidator
# Create your models here.

# this code defines a custom user model that extends Django's AbstractUser model. It adds a role field for user roles, sets default attributes for new users, and customizes the save method to assign the default role upon user creation.
class User(AbstractUser):
    class Role(models.TextChoices):
        USER = "USER", "User"

    email_validator = UnicodeUsernameValidator()
    base_role = Role.USER
    role = models.CharField(max_length=50, choices=Role.choices, null=True, blank=True)
    
    email = models.EmailField(
        ('email address'),
        max_length=150,
        unique=True,
        help_text=('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[email_validator],
        error_messages={
            'unique': ("A user with that email address already exists."),
        },
    )
    # This custom save method overrides the default save method. It checks if the user's primary key (pk) is not set, which indicates that the user is being created for the first time. If that's the case, it assigns the default role (base_role) to the user before calling the parent class's save method using super().
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
# Django's BaseUserManager class, which provides methods for managing user models that use email as the unique identifier instead of the default username.This custom manager allows you to retrieve only users with the "USER" role from the database. 
class UserTableManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.USER)
           
class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name="users", on_delete=models.CASCADE)
    email_verification = models.CharField(max_length=20, default="PENDING")
    is_password = models.BooleanField(default=True, max_length=10)

    def prefix(self):
        return "user-profile/" 
