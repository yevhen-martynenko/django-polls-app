from django import forms
from .models import Poll, Question, Option


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter Title', 'class': 'constructor__title'}),
            'description': forms.Textarea(attrs={'placeholder': 'Enter Description', 'class': 'constructor__description wrap-textarea', 'rows': '1'}),
        }

    def save(self, commit=True, *args, **kwargs):
        instance = super().save(commit=False, *args, **kwargs)
        instance.owner = self.user
        if commit:
            instance.save()
        return instance


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'


class OptionForm(forms.ModelForm):
    class Meta:
        model = Option
        fields = '__all__'
