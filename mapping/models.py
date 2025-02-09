from django.contrib.gis.db import models

class Shapefile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='shapefiles/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=255)
    geom = models.MultiPolygonField(srid=4326)  # or appropriate geometry field

    def __str__(self):
        return self.name