from django import forms
from .models import Habit

class HabitForm(forms.ModelForm):
    class Meta:
        model = Habit
        fields = ['name', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-indigo-400',
                'placeholder': 'e.g. Morning Workout'
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-3 py-2 border rounded focus:outline-none focus:ring focus:border-indigo-400',
                'rows': 3,
                'placeholder': 'Optional description'
            }),
        }
