import os
from django.contrib import admin
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.admin import GISModelAdmin  # Changed from OSMGeoAdmin
from .models import Shapefile, District
from django.core.files.storage import default_storage

@admin.register(Shapefile)
class ShapefileAdmin(admin.ModelAdmin):
    list_display = ("name", "uploaded_at")

    def save_model(self, request, obj, form, change):
        # Save the file first
        super().save_model(request, obj, form, change)
        
        # Get uploaded file path
        shapefile_path = obj.file.path
        
        try:
            # Read shapefile using GDAL
            ds = DataSource(shapefile_path)
            layer = ds[0]  # Get the first layer
            
            # Loop through features and save them in the District model
            for feature in layer:
                name = feature.get("name")  # Change field name based on your shapefile
                geom = feature.geom.geos  # Convert GDAL geometry to GEOS
                District.objects.create(name=name, geom=geom)
                
            # Optional: Delete the uploaded file after processing
            if os.path.exists(shapefile_path):
                os.remove(shapefile_path)
                
        except Exception as e:
            self.message_user(request, f"Error processing shapefile: {str(e)}", level='ERROR')


@admin.register(District)
class DistrictAdmin(GISModelAdmin):  # Changed from OSMGeoAdmin
    list_display = ("name",)
    
    # Optional: Configure map display settings
    default_lon = 0
    default_lat = 0
    default_zoom = 4
    map_width = 800
    map_height = 500