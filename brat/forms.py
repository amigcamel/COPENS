from django import forms
from brat.models import BratModel

FILE_SIZE_LIMIT = 2000 #kb

class BratModelForm(forms.ModelForm):

    class  Meta:
        model = BratModel
        fields = ('file_name', 'folder_name')
        widgets = {'folder_name': forms.TextInput(attrs={'readonly':'readonly'}),}

class UploadFile(forms.Form): 
    upload_file  = forms.FileField(help_text="File size limit: %d KB" % FILE_SIZE_LIMIT)

    def clean_upload_file(self):
        file_size_limit = FILE_SIZE_LIMIT * 1024
        upload_file = self.cleaned_data['upload_file']
        if upload_file == None:
            return upload_file
        if upload_file.content_type != 'text/plain':
            raise forms.ValidationError('You have to upload a text file')

        if upload_file.size > file_size_limit:
            raise forms.ValidationError('Please keep the file size under %d KB. Current size is %.1f KB.' % (FILE_SIZE_LIMIT, upload_file.size/1000.0))
        box = ''
        for chunk in upload_file.chunks():
            box += chunk
        try:
            box.decode('utf-8')
        except:
            raise forms.ValidationError('File should be encoded in utf-8')
        return box
