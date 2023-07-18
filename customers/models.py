import re
from xml.dom import ValidationErr
from django.db import models


# Create your models here.


def mobile_validator(value):
    # regex for validating a generic international phone number
    regex = r'^(\+|00){0,2}(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$'
    rule = re.compile(regex)
    if not rule.search(value):
        msg = "Invalid mobile number."
        raise ValidationErr(msg)


def email_validator(value):
    regex = ''
    rule = re.compile(regex)
    if not rule.search(value):
        msg = "Invalid email address."
        raise ValidationError(msg)


precidence_choices = (
    ("primary", "primary"),
    ("secondary", "secondary")
)


class Contacts(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=255, null=True, blank=True,
                              db_index=True, validators=[email_validator])
    mobile = models.CharField(max_length=32, null=True, blank=True,
                              db_index=True, validators=[mobile_validator])
    linkedId = models.ForeignKey(
        to="self", on_delete=models.CASCADE, null=True, blank=True)
    linkPrecidence = models.CharField(
        max_length=40, choices=precidence_choices)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)
    deleted_on = models.DateTimeField(auto_now=False, blank=True, null=True)

    def __str__(self) -> str:
        return super().__str__()
