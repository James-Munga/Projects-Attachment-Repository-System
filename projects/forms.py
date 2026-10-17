from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ["title", "code", "description", "department", "project_type", "status", "latitude", "longitude"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "latitude": forms.NumberInput(attrs={"step": "any", "placeholder": "-90 to 90"}),
            "longitude": forms.NumberInput(attrs={"step": "any", "placeholder": "-180 to 180"}),
        }

    def clean(self):
        cleaned = super().clean()
        lat, lon = cleaned.get("latitude"), cleaned.get("longitude")
        if (lat is None) != (lon is None):
            raise forms.ValidationError("Enter both latitude and longitude, or leave both blank.")
        if lat is not None and not (-90 <= lat <= 90):
            self.add_error("latitude", "Latitude must be between -90 and 90.")
        if lon is not None and not (-180 <= lon <= 180):
            self.add_error("longitude", "Longitude must be between -180 and 180.")
        return cleaned
