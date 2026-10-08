

# Register your models here.
from django.contrib import admin
from .models import Person, Union, ParentChild

admin.site.register(Person)
admin.site.register(Union)
admin.site.register(ParentChild)