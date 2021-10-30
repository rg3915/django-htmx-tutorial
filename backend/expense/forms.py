from django import forms

from .models import Expense


class ExpenseForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Expense
        fields = ('description', 'value')
        widgets = {
            'description': forms.TextInput(attrs={'placeholder': 'Descrição', 'autofocus': True}),
            'value': forms.NumberInput(attrs={'placeholder': 'Valor'}),
        }

    def __init__(self, *args, **kwargs):
        super(ExpenseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
