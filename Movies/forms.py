from django import forms
from django.forms import ModelForm

from Movies.models import Comment


class CommentCreateForm(ModelForm):
    class Meta:
        model = Comment
        fields = ("comment", "stars")

    comment = forms.CharField(
        required=False,
        label="comment",
        widget=forms.Textarea(attrs={"placeholder": "example input"}),
        max_length=1000,
    )
    stars = forms.FloatField(
        required=False,
        label="stars",
        widget=forms.NumberInput(
            attrs={
                "type": "range",
                "id": "form_homework",
                "class": "no_resize",
                "min": "0",
                "max": "10",
                "step": "0.1",
            }
        ),
    )

    def clean(self):
        cleaned_data = super().clean()
        # Always return cleaned_data
        return cleaned_data
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = " "
