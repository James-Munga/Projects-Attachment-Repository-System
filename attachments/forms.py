from django import forms
from .models import Attachment

MAX_UPLOAD_BYTES = 100 * 1024 * 1024

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ["title", "description", "file"]
        widgets = {"description": forms.Textarea(attrs={"rows": 2})}

    def clean_file(self):
        f = self.cleaned_data["file"]
        if f.size > MAX_UPLOAD_BYTES:
            raise forms.ValidationError("Each file must be 100 MB or smaller.")
        return f
