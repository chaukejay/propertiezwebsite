from django.db import models

# Create your models here.
class Integration(models.Model):
    # Name of integration eg: PropData / PropCtrl 
    name = models.CharField(max_length=100)
    # Whether the integration is enabled
    enabled = models.BooleanField(default=False)
    # Agent integration details
    api_key = models.CharField(null=True, blank=True, max_length=255)
    agent_id = models.CharField(null=True, blank=True, max_length=50)
    branch_id = models.CharField(null=True, blank=True, max_length=50)
    
    # Integration settings TODO
    # feed_leads = models.BooleanField(null=True, blank=True, default=False)
    # feed_listings = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self) -> str:
        return f"{self.name}: {self.enabled}"
    
def agency_image_upload_to(instance, filename):
    return f"agent_images/agencies/{instance.name}/{filename}"

class Agency(models.Model):
    name = models.CharField(null=False, blank=False, max_length=50)
    branch = models.CharField(null=False, blank=False, max_length=50)
    image = models.ImageField(upload_to=agency_image_upload_to, null=True, blank=True, default=None)
    
    def __str__(self) -> str:
        return f"{self.name}, {self.branch}"
    
    class Meta:
        verbose_name_plural = "Agencies"


def agent_image_upload_to(instance, filename):
    return f"agent_images/agents/{instance.first_name}_{instance.last_name}/{filename}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Agent(models.Model):
    # Personal details
    first_name = models.CharField(null=False, blank=False, max_length=50)
    last_name = models.CharField(null=False, blank=False, max_length=50)
    email = models.EmailField(null=False, blank=False, unique=True)
    contact_number = models.CharField(null=False, blank=False, unique=True, max_length=15) 
    ffc_id = models.CharField(null=False, blank=False, unique=True, max_length=20)

    publish_agent = models.BooleanField(default=True)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=agent_image_upload_to, null=True, blank=True, default=None)

    tags = models.ManyToManyField(Tag, related_name='agents', blank=True)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
