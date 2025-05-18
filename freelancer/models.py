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
    
class Bid(models.Model):
    id = models.BigIntegerField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bids')
    project_id = models.BigIntegerField()
    freelancer_id = models.BigIntegerField()
    bid_amount = models.FloatField()
    bid_message = models.TextField()
    created = models.DateTimeField()

    def __str__(self):
        return f"Bid {self.id} for {self.project.title}"