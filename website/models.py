from django.db import models


class Website(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title.title()
