from django.db import models
from django.core.exceptions import ValidationError

class City(models.Model):

    code = models.CharField(
        max_length=3,
        primary_key=True,
        verbose_name="City Code",
        help_text="Enter a unique 3-character code for the city.",
    )

    name = models.CharField(
        max_length=100,
        verbose_name="City Name",
        help_text="Enter the full name of the city.",
    )
    # Optional fields to store additional information about the city
    """
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Provide additional details about the city."
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Country",
        help_text="Enter the name of the country where the city is located."
    )
    """
    def clean(self):
        if len(self.code) != 3:
            raise ValidationError(f"City code must be exactly 4 characters. Got {len(self.code)} characters.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "City"
        verbose_name_plural = "Cities"
        ordering = ["name"]


class Hotel(models.Model):
    city = models.ForeignKey(
        City,
        on_delete=models.CASCADE,
        related_name="hotels",
        verbose_name="City",
        help_text="Select the city where the hotel is located.",
    )
    code = models.CharField(
        max_length=5,
        primary_key=True,
        verbose_name="Hotel Code",
        help_text="Enter a unique 5-character code for the hotel.",
    )
    name = models.CharField(
        max_length=100,
        verbose_name="Hotel Name",
        help_text="Enter the full name of the hotel.",
    )

    def clean(self):
        if len(self.code) != 5:
            raise ValidationError(f"Hotel code must be exactly 5 characters. Got {len(self.code)} characters.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
    
    # Optional fields to store additional information about the hotel
    """
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Provide additional details about the hotel."
    )
    
    # Optional field for the hotel's address
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Address",
        help_text="Enter the address of the hotel."
    )
    """

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        verbose_name = "Hotel"
        verbose_name_plural = "Hotels"
        ordering = ["name"]
