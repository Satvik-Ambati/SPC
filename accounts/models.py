from django.db import models
# from django.core.urlresolvers import reverse

# class Users(models.Model):
#     username = models.CharField(max_length=250)
#
# class Files(models.Model):
#     user = models.ForeignKey(Users, on_delete=models.CASCADE)
#     file_type = models.CharField(max_length=10)
#     file = models.FileField()

class ConsolePicture(models.Model):
   bytes = models.TextField()
   filename = models.CharField(max_length=255)
   mimetype = models.CharField(max_length=50)


class Document(models.Model):
   filename=models.CharField(max_length=255,blank=True)
   username = models.CharField(max_length=255)
   description = models.CharField(max_length=255, blank=True)
   document = models.FileField(upload_to='accounts.ConsolePicture/bytes/filename/mimetype', blank=True, null=True)
   uploaded_at = models.DateTimeField(auto_now_add=True)
