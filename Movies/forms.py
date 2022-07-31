from django import forms
from django.forms import ModelForm

from .models import Comment_movie, Comment_tv


class Comment_movie_CreateForm(ModelForm):
    class Meta:
        model = Comment_movie
        fields = ('comment', 'stars')

    comment = forms.CharField(required=False,label='comment',widget=forms.Textarea(
        attrs={'placeholder':'example input'}),max_length=1000)
    stars   = forms.FloatField(required=False,label='stars',widget=forms.NumberInput(
                            attrs={'type': 'range','id':'form_homework',"class": "no_resize",'min': '0','max':'10','step':'0.1'}))
    def clean(self):
        cleaned_data = super().clean()
        # Always return cleaned_data
        return cleaned_data
    def clean_stars(self):
        stars = self.cleaned_data['stars']
        if stars != None:
            if stars < 0 or stars > 10:
                raise forms.ValidationError("The rating input is incorrect.")
            return stars
        else:
            raise forms.ValidationError("The rating input is incorrect.")
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 1000:
            raise forms.ValidationError("There are too many characters.")
        elif len(comment) == 0:
            raise forms.ValidationError("Please enter the characters.")
        return comment
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.label_suffix=" "
        
class Comment_tv_CreateForm(ModelForm):
    class Meta:
        model = Comment_tv
        fields = ('comment', 'stars',)
    comment = forms.CharField(required=False,label='comment',widget=forms.Textarea(
        attrs={'placeholder':'example input'}),max_length=1000)
    stars   = forms.FloatField(required=False,label='stars',widget=forms.NumberInput(
       attrs={'type': 'range','id':'form_homework',"class": "no_resize",'min': '0','max':'10','step':'0.1'}))
    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data
    def clean_stars(self):
        stars = self.cleaned_data['stars']
        if stars != None:
            if stars < 0 or stars > 10:
                raise forms.ValidationError("The rating input is incorrect.")
            return stars
        else:
            raise forms.ValidationError("The rating input is incorrect.")
    def clean_comment(self):
        comment = self.cleaned_data['comment']
        if len(comment) > 1000:
            raise forms.ValidationError("There are too many characters.")
        elif len(comment) == 0:
            raise forms.ValidationError("Please enter the characters.")
        return comment
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.label_suffix=" "
        
    