from django import forms

from .models import Content, ClassContent, RaceContent, MonsterContent, SpellContent


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'category', 'description']

class ClassContentForm(forms.ModelForm):
    class Meta:
        model = ClassContent
        fields = ['hitPointsLevel1', 'hitPointsAboveLv1', 'hitDiceType', 'armorProficiency', 'shieldProficiency',
                  'weaponProficiency', 'toolProficiency', 'savingThrows', 'skills', 'abilities', 'archetypes']

class RaceContentForm(forms.ModelForm):
    class Meta:
        model = RaceContent
        fields = ['strScoreInc', 'dexScoreInc', 'conScoreInc', 'intScoreInc', 'wisScoreInc', 'chaScoreInc', 'age',
                  'alignment', 'size', 'speed', 'languages', 'abilities']

class MonsterContentForm(forms.ModelForm):
    class Meta:
        model = MonsterContent
        fields = ['armorClass', 'hitPoints', 'speed', 'strScore', 'dexScore', 'conScore', 'intScore', 'wisScore',
                  'chaScore', 'skills', 'passivePerception', 'challengeRate', 'xp', 'alignment', 'abilities', 'actions']

class SpellContentForm(forms.ModelForm):
    class Meta:
        model = SpellContent
        fields = ['level', 'castingTime', 'range', 'vComponent', 'sComponent', 'mComponent', 'duration', 'school']