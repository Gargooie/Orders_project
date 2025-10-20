from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['title', 'volume_type', 'description', 'document', 'quantity']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите наименование заказа'}),
            'volume_type': forms.RadioSelect(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Описание заказа'}),
            'document': forms.FileInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Количество'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].required = False
        self.fields['document'].required = False
        self.fields['quantity'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        volume_type = cleaned_data.get('volume_type')
        description = cleaned_data.get('description')
        document = cleaned_data.get('document')
        quantity = cleaned_data.get('quantity')
        
        if volume_type == 'single':
            if not description:
                raise forms.ValidationError('Для единичного заказа необходимо указать описание.')
        elif volume_type == 'multiple':
            if not document:
                raise forms.ValidationError('Для множественного заказа необходимо прикрепить документ.')
            if not quantity:
                raise forms.ValidationError('Для множественного заказа необходимо указать количество.')
        
        return cleaned_data
