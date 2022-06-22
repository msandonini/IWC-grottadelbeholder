from django import forms

from models import Content, ClassContent

class ContentForm(forms.Form):
    name = forms.CharField(max_length=30)
    description = forms.Textarea()
    category = forms.Select(choices=Content.Categories.choices)

class ClassContentForm(ContentForm):
    hitPointsLevel1 = forms.IntegerField(max_value=20, min_value=0)
    hitPointsAboveLv1 = forms.CharField(max_length=25)
    hitDiceType = forms.Select(ClassContent.DiceTypes.choices)