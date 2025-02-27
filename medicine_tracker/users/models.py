from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Represents a user's profile with additional personal and health-related information.
    Attributes:
        user (OneToOneField): A one-to-one relationship with the built-in Django User model.
        birth_date (DateField, optional): The user's birth date. Can be null or blank.
        health_condition (TextField, optional): Additional health-related information about the user.
    Methods:
        __str__(): Returns a string representation of the user profile, displaying the username.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    health_condition = models.TextField(blank=True)

    def __str__(self):
        """
        Returns:
            str: A string representation of the user's profile, showing the username.
        """
        return f"Profile: {self.user.username}"
