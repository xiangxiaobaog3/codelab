#-*- encoding:utf-8 -*-

from django import forms

class PriceInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        return '$ %s' % super(PriceInput, self).render(name, value, attrs)

class PercentInput(forms.TextInput):
    def render(self, name, value, attrs=None):
        return '%s %%' % super(PercentInput, self).render(name, value, attrs)

class ProductEntry(forms.Form):
    sku = forms.IntegerField(label='SKU')
    description = forms.CharField(widget=forms.Textarea())
    price = forms.DecimalField(decimal_places=2, widget=PriceInput())
    tax = forms.IntegerField(widget=PercentInput())

print ProductEntry()

