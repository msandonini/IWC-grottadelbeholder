from django import forms

from .models import Content, ClassContent, RaceContent, MonsterContent, SpellContent


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'category', 'description']
        labels = {
            'name': 'Nome',
            'category': 'Tipo',
            'description': 'Descrizione',
        }
        help_texts = {
        }
        error_messages = {
            'name': {
                'max_length': 'Nome troppo lungo'
            }
        }

class ClassContentForm(forms.ModelForm):
    class Meta:
        model = ClassContent
        fields = ['hitPointsLevel1', 'hitPointsAboveLv1', 'hitDiceType', 'armorProficiency', 'shieldProficiency',
                  'weaponProficiency', 'toolProficiency', 'savingThrows', 'skills', 'traits', 'archetypes']
        labels = {
            'hitPointsLevel1': 'Punti vita al livello 1',
            'hitPointsAboveLv1': 'Punti vita oltre il livello 1 (per livello)',
            'hitDiceType': 'Dado vita',
            'armorProficiency': 'Armature',
            'shieldProficiency': 'Scudo',
            'weaponProficiency': 'Armi',
            'toolProficiency': 'Attrezzi',
            'savingThrows': 'Tiri salvezza',
            'skills': 'Abilità',
            'traits': 'Tratti e caratteristiche',
            'archetypes': 'Archetipi',
        }
        help_texts = {

        }
        error_messages = {

        }

class RaceContentForm(forms.ModelForm):
    class Meta:
        model = RaceContent
        fields = ['strScoreInc', 'dexScoreInc', 'conScoreInc', 'intScoreInc', 'wisScoreInc', 'chaScoreInc', 'age',
                  'alignment', 'size', 'speed', 'languages', 'subraces']
        labels = {
            'strScoreInc': 'Aumento punteggio forza',
            'dexScoreInc': 'Aumento punteggio destrezza',
            'conScoreInc': 'Aumento punteggio costituzione',
            'intScoreInc': 'Aumento punteggio intelligenza',
            'wisScoreInc': 'Aumento punteggio saggezza',
            'chaScoreInc': 'Aumento punteggio carisma',
            'age': 'Età',
            'alignment': 'Allineamento',
            'size': 'Taglia',
            'speed': 'Velocità',
            'languages': 'Linguaggi',
            'subraces': 'Sottorazze',
        }
        help_texts = {

        }
        error_messages = {

        }

class MonsterContentForm(forms.ModelForm):
    class Meta:
        model = MonsterContent
        fields = ['armorClass', 'hitPoints', 'speed', 'strScore', 'dexScore', 'conScore', 'intScore', 'wisScore',
                  'chaScore', 'skills', 'passivePerception', 'challengeRate', 'xp', 'alignment', 'abilities', 'actions']
        labels = {

        }
        help_texts = {

        }
        error_messages = {

        }

class SpellContentForm(forms.ModelForm):
    class Meta:
        model = SpellContent
        fields = ['level', 'castingTime', 'range', 'vComponent', 'sComponent', 'mComponent', 'duration', 'school']
        labels = {

        }
        help_texts = {

        }
        error_messages = {

        }