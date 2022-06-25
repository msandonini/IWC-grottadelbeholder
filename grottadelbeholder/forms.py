from django import forms

from .models import Content, ClassContent, RaceContent, MonsterContent, SpellContent


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ['name', 'category', 'description']
        labels = {
            'name': 'Nome:',
            'category': 'Tipo:',
            'description': 'Descrizione:',
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
            'hitPointsLevel1': 'Punti vita al livello 1:',
            'hitPointsAboveLv1': 'Punti vita oltre il livello 1:',
            'hitDiceType': 'Dado vita:',
            'armorProficiency': 'Armature:',
            'shieldProficiency': 'Scudo:',
            'weaponProficiency': 'Armi:',
            'toolProficiency': 'Attrezzi:',
            'savingThrows': 'Tiri salvezza:',
            'skills': 'Abilità:',
            'traits': 'Tratti e caratteristiche:',
            'archetypes': 'Archetipi:',
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
            'strScoreInc': 'FOR',
            'dexScoreInc': 'DES',
            'conScoreInc': 'COS',
            'intScoreInc': 'INT',
            'wisScoreInc': 'SAG',
            'chaScoreInc': 'CAR',
            'age': 'Età:',
            'alignment': 'Allineamento:',
            'size': 'Taglia:',
            'speed': 'Velocità:',
            'languages': 'Linguaggi:',
            'subraces': 'Sottorazze:',
        }
        help_texts = {

        }
        error_messages = {

        }

class MonsterContentForm(forms.ModelForm):
    class Meta:
        model = MonsterContent
        fields = ['armorClass', 'hitPoints', 'speed', 'strScore', 'dexScore', 'conScore', 'intScore', 'wisScore',
                  'chaScore', 'passivePerception', 'skills', 'challengeRate', 'xp', 'alignment', 'traits', 'actions']
        labels = {
            'armorClass': 'Classe armatura',
            'hitPoints': 'Punti vita',
            'speed': 'Velocità',
            'strScore': 'FOR',
            'dexScore': 'DES',
            'conScore': 'COS',
            'intScore': 'INT',
            'wisScore': 'SAG',
            'chaScore': 'CAR',
            'passivePerception': 'Percezione passiva',
            'skills': 'Abilità',
            'challengeRate': 'Difficoltà',
            'xp': 'Exp',
            'alignment': 'Allineamento',
            'traits': 'Tratti',
            'actions': 'Azioni',
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
            'level': 'Livello',
            'castingTime': 'Tempo di lancio',
            'range': 'Raggio',
            'vComponent': 'V',
            'sComponent': 'S',
            'mComponent': 'M',
            'duration': 'Durata',
            'school': 'Scuola',
        }
        help_texts = {

        }
        error_messages = {

        }