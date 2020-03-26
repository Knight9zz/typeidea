from django import forms
from ckeditor_uploader.fields import RichTextUploadingFormField
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)