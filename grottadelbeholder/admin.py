from django.contrib import admin

# Register your models here.

from .models import *
admin.site.register(User)
admin.site.register(Admin)
admin.site.register(Content)
admin.site.register(RaceContent)
admin.site.register(ClassContent)
admin.site.register(MonsterContent)
admin.site.register(SpellContent)
admin.site.register(Review)