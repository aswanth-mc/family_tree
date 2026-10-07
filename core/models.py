import uuid
from django.db import models

# Create your models here.

class Person(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name=models.CharField(max_length=100)
    photo=models.ImageField(upload_to='photos/', null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Union(models.Model):
    id=models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    partner_1=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='union_as_p1')
    partner_2=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='union_as_p2')

class ParentChild(models.Model):
    union=models.ForeignKey(Union, on_delete=models.CASCADE, related_name='children', null=True, blank=True)
    child=models.ForeignKey(Person, on_delete=models.CASCADE, related_name='parents')