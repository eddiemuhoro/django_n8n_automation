from django.db import models

# Create your models here.
class Project(models.Model):
    id = models.BigIntegerField(primary_key=True)
    owner_id = models.BigIntegerField()
    title = models.CharField(max_length=255)
    url = models.URLField(max_length=200, blank=True, null=True)
    description = models.TextField()
    currency = models.CharField(max_length=10)
    created = models.DateTimeField()
    age_minutes = models.IntegerField()
    bid_count = models.IntegerField()
    bid_avg = models.FloatField()

    def __str__(self):
        return self.title