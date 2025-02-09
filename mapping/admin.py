import os
from django.contrib import admin
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.admin import GISModelAdmin
from django.core.files.storage import default_storage
from django.conf import settings
from .models import Shapefile, District

@admin.register(Shapefile)
class ShapefileAdmin(admin.ModelAdmin):
    list_display = ("name", "uploaded_at")

    def save_model(self, request, obj, form, change):
        # Save the file first
        super().save_model(request, obj, form, change)

        # Get the correct file path using default_storage
        file_path = obj.file.name
        absolute_path = os.path.join(settings.MEDIA_ROOT, file_path)
        print("its save ")
        try:
            # Ensure the file exists
            if not default_storage.exists(file_path):
                raise ValueError(f"File not found at {file_path}")

            # Read shapefile using GDAL with absolute path
            ds = DataSource(absolute_path)
            
            if len(ds) == 0:
                raise ValueError("Shapefile contains no layers")
                
            layer = ds[0]  # Get the first layer
            
            # Print available fields for debugging
            print(f"Available fields: {layer.fields}")
            
            # Loop through features and save them in the District model
            for feature in layer:
                # Try multiple common field names for the district name
                name = None
                name_fields = ['name', 'NAME', 'Name', 'DISTRICT', 'District']
                
                for field in name_fields:
                    try:
                        if field in feature.fields:
                            name = feature.get(field)
                            break
                    except:
                        continue
                
                if name is None:
                    print(f"Warning: Could not find name field for feature. Available fields: {feature.fields}")
                    continue

                try:
                    geom = feature.geom.geos
                    District.objects.create(name=name, geom=geom)
                except Exception as e:
                    print(f"Error processing feature {name}: {str(e)}")
                    continue

            self.message_user(request, f"Successfully processed shapefile: {obj.name}")

        except Exception as e:
            self.message_user(
                request, 
                f"Error processing shapefile: {str(e)}\nFile path: {absolute_path}", 
                level='ERROR'
            )
            # Don't remove file on error so it can be debugged
            return

        # Only remove file if processing was successful
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
        except Exception as e:
            self.message_user(
                request,
                f"Warning: Could not remove processed file: {str(e)}",
                level='WARNING'
            )

@admin.register(District)
class DistrictAdmin(GISModelAdmin):
    list_display = ("name",)
    
    # Map display settings
    default_lon = 78.9629  # Roughly center of India
    default_lat = 20.5937
    default_zoom = 5
    map_width = 800
    map_height = 500

    # Optional: Add search and filtering
    search_fields = ['name']
    list_filter = ['name']