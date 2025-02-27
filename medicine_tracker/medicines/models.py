from django.db import models
from django.contrib.auth.models import User


"""
This module defines models for managing medicines and their dosage options in a Django application.
Constants:
    DOSAGE_CHOICES (list of tuples): A predefined list of common dosage options.
Models:
    - Medicine: Represents a medication with a unique name.
    """
DOSAGE_CHOICES = [
        ("1 tablet", "1 tablet"),
        ("2 tablets", "2 tablets"),
        ("3 tablets", "3 tablets"),
        ("5 ml", "5 ml"),
        ("10 ml", "10 ml"),
        ("15 ml", "15 ml"),
        ("1 capsule", "1 capsule"),
        ("2 capsules", "2 capsules"),
        ("3 capsules", "3 capsules"),
    ]

class Medicine(models.Model):
    name = models.CharField(max_length=100, unique=True)
    storage_temp = models.CharField(max_length=50, blank=True)
    side_effects = models.TextField(blank=True, null=True)
    manufacturer = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Comment(models.Model):
    """
        Model for storing user comments on medicines.

        This model allows users to leave comments on specific medicines.
        Each comment is associated with a user, a medicine, and a timestamp of when it was created.

        Attributes:
            user (ForeignKey): Reference to the user who wrote the comment.
            medicine (ForeignKey): Reference to the medicine the comment is related to.
            text (TextField): The content of the comment.
            created_at (DateTimeField): The timestamp when the comment was created (automatically set upon creation).

        Methods:
            __str__(): Returns a string representation of the comment in the format "user to medicine".
        """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name="comments")
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} k {self.medicine.name}"


class UserMedicine(models.Model):
    """
    Represents a user's specific medication with dosage and schedule.

    Attributes:
        user (ForeignKey): References the user who owns the medication.
        medicine (ForeignKey): References the associated medicine.
        dosage (CharField): Specifies the dosage of the medication.
        notes (TextField, optional): Additional notes regarding the medication.
        day (DateField, optional): The scheduled day for taking the medication.
        time (TimeField, optional): The scheduled time for taking the medication.
        remaining_doses (IntegerField): Number of doses left, defaults to 0.
     Methods:
        __str__(): Returns a string representation of the user's medication.
        take_dose(): Decreases the remaining doses by one if available.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100,choices=DOSAGE_CHOICES, default="1 tablet")
    notes = models.TextField(blank=True, null=True)
    day = models.DateField(blank=True, null=True)
    time = models.TimeField(blank=True, null=True)
    remaining_doses = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the user's medication,
        including the remaining dose count.
        """
        return f"{self.user.username} - {self.medicine} ({self.remaining_doses} doses)"

    def take_dose(self):
        """
        Decreases the remaining doses by one if available.
        Returns:
            bool: True if a dose was taken, False if no doses remain.
        """
        if self.remaining_doses > 0:
            self.remaining_doses -= 1
            self.save()
            return True
        return False


class MedicineHistory(models.Model):
    """
    Records the history of medication intake by the user.
     Attributes:
        user_medicine (ForeignKey): References the specific medication taken.
        date (DateTimeField): Timestamp when the medication was taken.
     Methods:
        __str__(): Returns a formatted string of the medicine intake event.
    """
    user_medicine = models.ForeignKey(UserMedicine, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Returns a string representation of the medicine intake event,
        formatted as "Medicine Name taken on DD.MM.YYYY HH:MM".
        """
        return f"{self.user_medicine.medicine.name} taken on {self.date.strftime('%d.%m.%Y %H:%M')}"


class MedicineInteraction(models.Model):
    """
    Represents interactions between multiple medicines.

    Attributes:
        medicines (ManyToManyField): A many-to-many relationship with the Medicine model.
        description (TextField): A detailed description of the interaction.
    Methods:
        __str__(): Returns a string representation of the interaction, listing involved medicines.
    """

    medicines = models.ManyToManyField(Medicine)
    description = models.TextField()

    def __str__(self):
        """
        Returns a string representation of the medicine interaction.
        If medicines are present, it lists them in the format:
        "Interaction between [Medicine1, Medicine2, ...]".
        Otherwise, it returns a general label "Medicine Interaction".
        """
        medicines_list = ", ".join(med.name for med in self.medicines.all())
        return f"Interaction between {medicines_list}" if medicines_list else "Medicine Interaction"

