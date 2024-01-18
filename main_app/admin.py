from django.contrib import admin
# improt finch model
from.models import Finch, Feeding, Toy, Photo
# Register your models here.
admin.site.register(Finch)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)
