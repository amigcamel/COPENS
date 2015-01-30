from django.db import models

class BratModel(models.Model):
#    upload_file = models.FileField()
    file_name = models.CharField(max_length=100)
    folder_name = models.CharField(max_length=100)
    user_name = models.CharField(max_length=100)

