from django import forms
from .models import SearchPortfolio

class XlsxImportForm(forms.Form):
  xlsx_file = forms.FileField()

class XlsxImportSearchTermForm(forms.Form):
  xlsx_file = forms.FileField()
  portfolio = forms.ChoiceField(choices = [(portfolio.pk, portfolio.name) for portfolio in SearchPortfolio.objects.all()])