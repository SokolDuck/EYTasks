from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(allow_empty_file=True)

    def __init__(self, data=None, files=None):
        super().__init__(data=data, files=files)