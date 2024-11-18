from django import forms
from .models import Car, Comment


class CarForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = ('make', 'model', 'year', 'description')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
        labels = {
            'content': 'Содержание комментария',
        }
        help_texts = {
            'content': 'Введите содержание комментария (минимум 10 символов)',
        }
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5, 'cols': 50}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['content'].validators.append(forms.MinLengthValidator(10))