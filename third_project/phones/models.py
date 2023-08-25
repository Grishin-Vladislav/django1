from django.db import models
from django.utils.text import slugify


class Phone(models.Model):
    name = models.CharField(max_length=60)
    price = models.FloatField()
    image = models.URLField()
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.TextField()

    def save(
            self, force_insert=False, force_update=False, using=None,
            update_fields=None
    ):
        self.slug = slugify(self.name)
        if update_fields is not None and "name" in update_fields:
            update_fields = {"slug"}.union(update_fields)
        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )