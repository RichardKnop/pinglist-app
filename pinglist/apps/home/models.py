from django.db import models


class FAQ(models.Model):

    question = models.TextField()
    answer = models.TextField()

    def __unicode__(self):
        return self.question