from django.contrib import admin
from .models import Medicine, UserMedicine, MedicineHistory, MedicineInteraction, Comment

admin.site.register(Medicine)
admin.site.register(UserMedicine)
admin.site.register(MedicineHistory)
admin.site.register(MedicineInteraction)
admin.site.register(Comment)
