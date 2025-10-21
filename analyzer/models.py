from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models import JSONField
from decimal import Decimal
import hashlib
from django.utils import timezone


def convert_decimal(obj):
    if isinstance(obj, list):
        return [convert_decimal(i) for i in obj]
    elif isinstance(obj, dict):
        return {k: convert_decimal(v) for k, v in obj.items()}
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj


class AnalyzedString(models.Model):
    id = models.CharField(max_length=64, primary_key=True, editable=False)
    value = models.TextField(unique=True)
    properties = JSONField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = hashlib.sha256(self.value.encode('utf-8')).hexdigest()
        self.properties = convert_decimal(self.properties)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.value[:30]


