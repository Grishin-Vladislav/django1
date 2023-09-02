from django.db import models


class Sensor(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        on_delete=models.CASCADE,
        null=False,
        related_name='measurements'
    )
    temperature = models.IntegerField(null=False)
    date = models.DateTimeField(null=False, auto_now_add=True)


