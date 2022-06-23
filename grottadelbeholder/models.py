from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


# Create your models here.
class User(models.Model):
    mail = models.EmailField(unique=True)
    username = models.CharField(max_length=25, unique=True)
    password = models.CharField(max_length=64)       # Da criptare nel codice di input

    def __str__(self):
        return self.username + " - " + self.mail


class Admin(models.Model):

    class AdminType(models.TextChoices):
        KOBOLD = "KO", "Kobold"
        DRAGONBORN = "DB", "Dragonborn"
        BEHOLDER = "BH", "Beholder"
        DUNGEONMASTER = "DM", "Dungeon Master"



    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE)
    type = models.CharField(choices=AdminType.choices, max_length=2, default=AdminType.KOBOLD)

    def __str__(self):
        return self.type + ": " + str(self.user)


class Content(models.Model):

    class Categories(models.TextChoices):
        CLASSES = "CL", "Classi"
        RACES = "RA", "Razze"
        MONSTERS = "MO", "Mostri"
        SPELLS = "SP", "Incantesimi"

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.CharField(choices=Categories.choices, max_length=2, default=None)
    pub_date = models.DateTimeField("date published")      # Da inserire automaticamente all'inserimento
    rev = models.IntegerField(default=1)                   # Da incrementare automaticamente alla modifica

    name = models.CharField(max_length=30)
    description = models.TextField()

    def __str__(self):
        return self.name + " by " + str(self.user) + " (" + self.category + ")"


class ClassContent(models.Model):

    class ArmorProficiencies(models.TextChoices):
        NONE = "N", "Nessuna"
        LIGHT = "L", "Armature leggere"
        MEDIUM = "M", "Armature medie"
        ALL = "A", "Tutte le armature"

    class DiceTypes(models.TextChoices):
        D4 = "4", "1d4"
        D6 = "6", "1d6"
        D8 = "8", "1d8"
        D10 = "10", "1d10"
        D12 = "12", "1d12"
        D20 = "20", "1d20"

    content = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

    # HIT POINTS
    hitPointsLevel1 = models.PositiveSmallIntegerField(validators=[MaxValueValidator(20)])
    hitPointsAboveLv1 = models.CharField(max_length=25)
    hitDiceType = models.CharField(max_length=5, choices=DiceTypes.choices)       # Per level

    # PROFICIENCIES
    armorProficiency = models.CharField(choices=ArmorProficiencies.choices, max_length=1)
    shieldProficiency = models.BooleanField()
    weaponProficiency = models.CharField(max_length=100)
    toolProficiency = models.CharField(max_length=100)

    savingThrows = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)

    traits = models.TextField()

    archetypes = models.TextField()

    def __str__(self):
        return str(self.content)


class RaceContent(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

    scoreIncValidators = [
        MinValueValidator(-4),
        MaxValueValidator(4)
    ]

    strScoreInc = models.SmallIntegerField(validators=scoreIncValidators)
    dexScoreInc = models.SmallIntegerField(validators=scoreIncValidators)
    conScoreInc = models.SmallIntegerField(validators=scoreIncValidators)
    intScoreInc = models.SmallIntegerField(validators=scoreIncValidators)
    wisScoreInc = models.SmallIntegerField(validators=scoreIncValidators)
    chaScoreInc = models.SmallIntegerField(validators=scoreIncValidators)

    age = models.CharField(max_length=200)
    alignment = models.CharField(max_length=200)
    size = models.CharField(max_length=200)
    speed = models.CharField(max_length=200)
    languages = models.CharField(max_length=200)

    subraces = models.TextField()

    def __str__(self):
        return str(self.content)


class MonsterContent(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

    armorClass = models.PositiveSmallIntegerField(default=15, validators=[
                                         MaxValueValidator(25),
                                         MinValueValidator(1)
                                     ])
    hitPoints = models.PositiveSmallIntegerField()
    speed = models.PositiveSmallIntegerField()

    scoreValidators = [
        MinValueValidator(1),
        MaxValueValidator(30)
    ]

    strScore = models.PositiveSmallIntegerField(validators=scoreValidators)
    dexScore = models.PositiveSmallIntegerField(validators=scoreValidators)
    conScore = models.PositiveSmallIntegerField(validators=scoreValidators)
    intScore = models.PositiveSmallIntegerField(validators=scoreValidators)
    wisScore = models.PositiveSmallIntegerField(validators=scoreValidators)
    chaScore = models.PositiveSmallIntegerField(validators=scoreValidators)

    skills = models.TextField()
    passivePerception = models.PositiveSmallIntegerField(validators=scoreValidators)

    challengeRate = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(30)
    ])
    xp = models.PositiveIntegerField()

    alignment = models.CharField(max_length=200)

    abilities = models.TextField()
    actions = models.TextField()

    def __str__(self):
        return str(self.content)


class SpellContent(models.Model):
    class SchoolTypes(models.TextChoices):
        EVOCATION = "V", "Evocazione"
        ILLUSION = "I", "Illusione"
        CONJURATION = "C", "Invocazione"
        ABJURATION = "A", "Abiurazione"
        NECROMANCY = "N", "Necromanzia"
        TRANSMUTATION = "T", "Trasmutazione"
        ENCHANTMENT = "E", "Ammaliamento"
        DIVINATION = "D", "Divinazione"

    content = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

    level = models.PositiveSmallIntegerField(validators=[MaxValueValidator(12)])

    castingTime = models.CharField(max_length=25)
    range = models.CharField(max_length=25)
    vComponent = models.BooleanField()
    sComponent = models.BooleanField()
    mComponent = models.BooleanField()
    duration = models.CharField(max_length=25)

    school = models.CharField(choices=SchoolTypes.choices, max_length=1, default=SchoolTypes.EVOCATION)

    def __str__(self):
        return str(self.content)


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    vote = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()

    def __str__(self):
        return str(self.user) + " -> " + str(self.content) + " - " + str(self.vote) + ": " + self.comment
