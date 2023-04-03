from django.contrib import admin
from home.models import User,Contact,Service,Worker
# Register your models here.


admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Service)
admin.site.register(Worker)