from django.db import models
from django.core.exceptions import ValidationError
import tracking.models
import re
import string
import typing

_digits_re = re.compile(r'^[0-9]+$')


def validate_imei(value):
    if not bool(_digits_re.match(value)):
        raise ValidationError("IMEI must be a number")
    if len(value) != 15:
        raise ValidationError("IMEI must be 15 digits long")


def validate_aes_key(value):
    if not value:
        return

    if not all(c in string.hexdigits for c in value):
        raise ValidationError("AES key must be a hex string")

    if len(value) != 64:
        raise ValidationError("AES key must be 32 bytes long")


class Tracker(models.Model):
    MODEL_TRACK24 = "track24"
    MODEL_NAL = "nal"

    MODELS = (
        (MODEL_TRACK24, "Track24"),
        (MODEL_NAL, "NAL Research"),
    )

    id = models.UUIDField(primary_key=True, editable=False, unique=True, default=uuid.uuid4)
    model = models.CharField(max_length=255, choices=MODELS)
    name = models.CharField(max_length=255)
    imei = models.CharField(max_length=15, unique=True, validators=[validate_imei], verbose_name="IEMI")
    aes_encryption_key = models.CharField(
        blank=True, null=True, max_length=64, validators=[validate_aes_key],
        verbose_name="AES encryption key"
    )
    aes_decryption_key = models.CharField(
        blank=True, null=True, max_length=64, validators=[validate_aes_key],
        verbose_name="AES decryption key"
    )

    vehicle = models.OneToOneField(
        tracking.models.Vehicle, on_delete=models.SET_NULL, blank=True, null=True, related_name="tracker"
    )

    class Meta:
        indexes = [
            models.Index(fields=["imei"]),
        ]

    def __str__(self):
        return self.name

    def aes_encryption_key_bytes(self) -> typing.Optional[bytes]:
        if self.aes_encryption_key:
            return bytes.fromhex(self.aes_encryption_key)
        else:
            return None

    def aes_decryption_key_bytes(self) -> typing.Optional[bytes]:
        if self.aes_decryption_key:
            return bytes.fromhex(self.aes_decryption_key)
        else:
            return None

    def vehicle_opt(self) -> typing.Optional[Vehicle]:
        try:
            return self.vehicle
        except ObjectDoesNotExist:
            return None