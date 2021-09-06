from django import forms

from .models import Book


class BookForm(forms.ModelForm):
    required_css_class = 'required'

    class Meta:
        model = Book
        fields = ('title', 'author')

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
