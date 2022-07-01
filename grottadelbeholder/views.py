from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from django.views import View

from .models import User, Admin, Content
from .forms import *

import hashlib

LOGGED_USER_ID = 'loggedUserID'
LOGGED_USER_NAME = 'loggedUser'
ADMIN_TYPE_KEY = 'adminType'

FILTER_ALL = "all"

N_CONTENT_PAGE = 25

class IndexView(View):
    template_name = "grottadelbeholder/index.html"


    def get(self, request):
        context = contextSetup(request)

        context['filterRaces'] = Content.Categories.RACES
        context['filterClasses'] = Content.Categories.CLASSES
        context['filterMonsters'] = Content.Categories.MONSTERS
        context['filterSpells'] = Content.Categories.SPELLS
        context['filterAll'] = FILTER_ALL


        if 'filter' in request.GET:
            filter = request.GET["filter"]
            context['filter'] = filter

            contentList = []

            page = 0
            if 'page' in request.GET:
                page = request.GET['page']

            context['page'] = page

            if filter == Content.Categories.RACES:
                context['npages'] = Content.objects.count() / N_CONTENT_PAGE

                for content in Content.objects.get(category=Content.Categories.RACES)[(N_CONTENT_PAGE * page):(N_CONTENT_PAGE * (page + 1))]:
                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': content.category,
                        'user': content.user.username
                    })
            elif filter == Content.Categories.CLASSES:
                pass
            elif filter == Content.Categories.MONSTERS:
                pass
            elif filter == Content.Categories.SPELLS:
                pass
            elif filter == FILTER_ALL:
                for content in Content.objects.all():


                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': content.category,
                        'user': content.user.username
                    })
            else:
                return render(request, self.template_name, context)

            context['contentList'] = contentList

            return render(request, self.template_name, context)

        return render(request, self.template_name, context)

class ReviewView(View):
    template_name = "grottadelbeholder/review.html"

    def get(self, request):
        context = contextSetup(request)

        if userIsLogged(request):
            return "ok"

        return "none"

class SigninView(View):
    template_name = "grottadelbeholder/signin.html"

    def get(self, request):
        context = {}

        if userIsLogged(request):
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if userIsLogged(request):
            return HttpResponseRedirect(redirect_to="./")

        if ("email" in request.POST) and ("username" in request.POST) and ("password" in request.POST):
            email = request.POST["email"]
            username = request.POST["username"]
            password = request.POST["password"]

            users = User.objects.all()
            emailInDb = False
            usernameInDb = False
            for user in users:
                if email == user.mail:
                    emailInDb = True
                    break
                if username == user.username:
                    usernameInDb = True
                    break

            if emailInDb:
                context["msg"] = "Email già associata a un account"
            elif usernameInDb:
                context["msg"] = "Username già associato a un account"

            if "msg" not in context:
                password = hashlib.sha256(password.encode()).digest()

                user = User(mail=email, username=username, password=password)
                user.save()

                request.session[LOGGED_USER_ID] = user.id
                request.session[LOGGED_USER_NAME] = username
                context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
                return HttpResponseRedirect(redirect_to="./")
        else:
            context["msg"] = "Inserire valori validi"

        return render(request, self.template_name, context)

class LoginView(View):
    template_name = "grottadelbeholder/login.html"

    def get(self, request):
        context = {}

        if LOGGED_USER_ID in request.session:
            context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
            return HttpResponseRedirect(redirect_to="./")

        return render(request, self.template_name, context)

    def post(self, request):
        context = {}

        if userIsLogged(request):
            context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)
            return HttpResponseRedirect(redirect_to="./")

        context = {}

        if "username" in request.POST and "password" in request.POST:
            userMailOrName = request.POST["username"]
            password = str(hashlib.sha256(request.POST["password"].encode()).digest())

            print("Username or mail: " + userMailOrName)
            print("Password: " + password)
            for user in User.objects.all():
                print(user.mail)
                print(user.username)
                print(user.password)
                if user.mail == userMailOrName or user.username == userMailOrName:
                    if password == user.password:
                        request.session[LOGGED_USER_NAME] = user.username
                        request.session[LOGGED_USER_ID] = user.id
                        context[LOGGED_USER_NAME] = request.session.get(LOGGED_USER_NAME)

                        return HttpResponseRedirect(redirect_to="./")
                    else:
                        context["msg"] = "Password errata"
                        break
            if "msg" not in context:
                context["msg"] = "Utente non registrato"
        else:
            context["msg"] = "Inserire valori validi"

        return render(request, self.template_name, context)

class LogoutView(View):

    def get(self, request):
        if LOGGED_USER_ID in request.session:
            del request.session[LOGGED_USER_ID]

        if LOGGED_USER_NAME in request.session:
            del request.session[LOGGED_USER_NAME]

        return HttpResponseRedirect(redirect_to="./")

class InfoView(View):
    template_name = "grottadelbeholder/info.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)

# TODO UserView
class UserView(View):
    template_name = "grottadelbeholder/user.html"

    def get(self, request):

        if not userIsLogged(request):
            return HttpResponseRedirect(redirect_to="grottadelbeholder/login.html")

        context = contextSetup(request)

        return render(request, self.template_name, context)

# TODO AdminView
class AdminView(View):
    template_name = "grottadelbeholder/admin.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)

class CreateContentView(View):
    template_name = "grottadelbeholder/create.html"

    def get(self, request):
        context = contextSetup(request)

        context['contentForm'] = ContentForm()
        context['classForm'] = ClassContentForm()
        context['raceForm'] = RaceContentForm()
        context['monsterForm'] = MonsterContentForm()
        context['spellForm'] = SpellContentForm()

        return render(request, self.template_name, context)

    def post(self, request):

        context = contextSetup(request)

        contentForm = ContentForm(request.POST)
        context['contentForm'] = contentForm

        detailForm = None

        category = request.POST['category']

        if category == Content.Categories.RACES:
            detailForm = RaceContentForm(request.POST)
            context['raceForm'] = detailForm
            context['selectedForm'] = 'raceForm'

            context['classForm'] = ClassContentForm()
            context['monsterForm'] = MonsterContentForm()
            context['spellForm'] = SpellContentForm()

        elif category == Content.Categories.CLASSES:
            detailForm = ClassContentForm(request.POST)
            context['classForm'] = detailForm
            context['selectedForm'] = 'classForm'

            context['raceForm'] = RaceContentForm()
            context['monsterForm'] = MonsterContentForm()
            context['spellForm'] = SpellContentForm()

        elif category == Content.Categories.MONSTERS:
            detailForm = MonsterContentForm(request.POST)
            context['monsterForm'] = detailForm
            context['selectedForm'] = 'monsterForm'

            context['classForm'] = ClassContentForm()
            context['raceForm'] = RaceContentForm()
            context['spellForm'] = SpellContentForm()

        elif category == Content.Categories.SPELLS:
            detailForm = SpellContentForm(request.POST)
            context['spellForm'] = detailForm
            context['selectedForm'] = 'spellForm'

            context['classForm'] = ClassContentForm()
            context['raceForm'] = RaceContentForm()
            context['monsterForm'] = MonsterContentForm()

        else:
            context['message'] = 'Errore: categoria non esistente'
            return render(request, self.template_name, context)

        if not userIsLogged(request):
            context['message'] = 'Errore: devi essere registrato per inserire un nuovo contenuto'
            return render(request, self.template_name, context)

        if not contentForm.is_valid():
            context['message'] = 'Errore: Le informazioni generali non sono valide'

            return render(request, self.template_name, context)

        print(request.POST)

        if not detailForm.is_valid():
            context['message'] = 'Errore: I dati inseriti non sono vaildi'
            return render(request, self.template_name, context)

        content = Content(
            user = (User.objects.get(id=request.session.get(LOGGED_USER_ID))),
            category = request.POST['category'],
            rev = 1,
            pub_date = timezone.now(),
            name = request.POST['name'],
            description = request.POST['description']
        )
        print(content)
        content.save()
        detailContent = None

        # TODO trovare un modo per poter separare i valori con nome uguale nella post

        if category == Content.Categories.RACES:
            detailContent = RaceContent(
                content = content,
                strScoreInc = request.POST['strScoreInc'],
                dexScoreInc = request.POST['dexScoreInc'],
                conScoreInc = request.POST['conScoreInc'],
                intScoreInc = request.POST['intScoreInc'],
                wisScoreInc = request.POST['wisScoreInc'],
                chaScoreInc = request.POST['chaScoreInc'],
                age = request.POST['age'],
                alignment = request.POST['alignment'],
                size = request.POST['size'],
                speed = request.POST['speed'],
                languages = request.POST['languages'],
                subraces = request.POST['subraces']
            )
        elif category == Content.Categories.CLASSES:
            detailContent = ClassContent(
                content = content,
                hitPointsLevel1 = request.POST['hitPointsLevel1'],
                hitPointsAboveLv1 = request.POST['hitPointsAboveLv1'],
                hitDiceType = request.POST['hitDiceType'],
                armorProficiency = request.POST['armorProficiency'],
                shieldProficiency = request.POST['shieldProficiency'],
                weaponProficiency = request.POST['weaponProficiency'],
                toolProficiency = request.POST['toolProficiency'],
                savingThrows = request.POST['savingThrows'],
                skills = request.POST['skills'],
                traits = request.POST['traits'],
                archetypes = request.POST['archetypes']
            )
        elif category == Content.Categories.MONSTERS:
            detailContent = MonsterContent (
                content = content,
                armorClass = request.POST['armorClass'],
                hitPoints = request.POST['hitPoints'],
                speed = request.POST['speed'],
                strScore = request.POST['strScore'],
                dexScore = request.POST['dexScore'],
                conScore = request.POST['conScore'],
                intScore = request.POST['intScore'],
                wisScore = request.POST['wisScore'],
                chaScore = request.POST['chaScore'],
                passivePerception = request.POST['passivePerception'],
                skills = request.POST['skills'],
                challengeRate = request.POST['challengeRate'],
                xp = request.POST['xp'],
                alignment = request.POST['alignment'],
                traits = request.POST['traits'],
                actions = request.POST['actions'],
            )
        elif category == Content.Categories.SPELLS:
            detailContent = SpellContent(
                content=content,
                level = request.POST['level'],
                castingTime = request.POST['castingTime'],
                range = request.POST['range'],
                vComponent = request.POST['vComponent'],
                sComponent = request.POST['sComponent'],
                mComponent = request.POST['mComponent'],
                duration = request.POST['duration'],
                school = request.POST['school'],
            )

        detailContent.save()

        # TODO Redirect alla pagina del contenuto appena creato
        return HttpResponse("Contenuto creato")

# TODO ModifyContentView
class ModifyContentView(View):
    template_name = "grottadelbeholder/modify.html"

    def get(self, request):
        pass
    def post(self, request):
        pass

# TODO UserContentView
class UserContentView(View):
    template_name = "grottadelbeholder/usercontent.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)



def contextSetup(request):
    context = {}

    if userIsLogged(request):
        context[LOGGED_USER_NAME] = User.objects.get(id=request.session[LOGGED_USER_ID]).username

    adminType = userAdminType(request)

    if not adminType is None:
        context[ADMIN_TYPE_KEY] = adminType

    return context

def userIsLogged(request):
    if LOGGED_USER_ID in request.session:
        return True
    return False

def userAdminType(request):
    admins = Admin.objects.all()

    if userIsLogged(request):
        for admin in admins:
            if admin.user_id == request.session[LOGGED_USER_ID]:
                return admin.type

    return None