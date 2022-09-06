import json
import mimetypes

from django.core.files.base import ContentFile
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.utils import timezone

from django.views import View

from .models import User, Admin
from .forms import *

import hashlib
import requests

LOGGED_USER_ID = 'loggedUserID'
LOGGED_USER_NAME = 'loggedUser'
ADMIN_TYPE_KEY = 'adminType'

FILTER_ALL = "all"

N_CONTENT_PAGE = 25

class IndexView(View):
    template_name = "grottadelbeholder/index.html"
    detail_template_name = "grottadelbeholder/detail.html"

    def get(self, request):
        context = contextSetup(request)

        context['filterRaces'] = Content.Categories.RACES
        context['filterClasses'] = Content.Categories.CLASSES
        context['filterMonsters'] = Content.Categories.MONSTERS
        context['filterSpells'] = Content.Categories.SPELLS
        context['filterAll'] = FILTER_ALL

        if 'detail' in request.GET:
            detailId = request.GET['detail']
            if 'filter' in request.GET:
                context['filter'] = request.GET['filter']
            if 'page' in request.GET:
                context['page'] = request.GET['page']

            if 'download' in request.GET and request.GET['download'] == True:
                # TODO Permettere download contenuto
                pass

            content = Content.objects.get(id=detailId)
            detailContent = None

            context['content'] = content
            context['category'] = Content.Categories(content.category).label.capitalize()

            if content.category == Content.Categories.RACES and RaceContent.objects.filter(content_id=content.id).exists():
                detailContent = RaceContent.objects.get(content = content)
            elif content.category == Content.Categories.CLASSES and ClassContent.objects.filter(content_id=content.id).exists():
                detailContent = ClassContent.objects.get(content = content)
                context["armorProficiency"] = ClassContent.ArmorProficiencies(detailContent.armorProficiency).label
            elif content.category == Content.Categories.MONSTERS and MonsterContent.objects.filter(content_id=content.id).exists():
                detailContent = MonsterContent.objects.get(content = content)
            elif content.category == Content.Categories.SPELLS and SpellContent.objects.filter(content_id=content.id).exists():
                detailContent = SpellContent.objects.get(content = content)
            else:
                context['message'] = "A quanto pare questo contenuto non è effettivamente presente. Vi preghiamo di segnalarcelo alle informazioni di contatto. Ci scusiamo per il disagio"

            context['detailContent'] = detailContent

            return render(request, self.detail_template_name, context)

        if 'filter' in request.GET:
            filter = request.GET['filter']

            if filter == 'user':
                return HttpResponseRedirect(redirect_to="/grottadelbeholder/usercontent")

            context['filter'] = filter

            contentList = []

            page = 1
            npages = 1
            if 'page' in request.GET:
                page = int(request.GET['page'])

            if filter == Content.Categories.RACES:
                npages = int(1 + Content.objects.filter(category=Content.Categories.RACES).count() / N_CONTENT_PAGE)

                list = Content.objects.filter(category=Content.Categories.RACES)[N_CONTENT_PAGE * (page - 1) : N_CONTENT_PAGE * page]
                for content in list:
                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': Content.Categories(content.category).label.capitalize(),
                        'user': content.user.username,
                        'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                        'rev': content.rev
                    })
            elif filter == Content.Categories.CLASSES:
                npages = int(1 + Content.objects.filter(category=Content.Categories.CLASSES).count() / N_CONTENT_PAGE)

                list = Content.objects.filter(category=Content.Categories.CLASSES)[
                       N_CONTENT_PAGE * (page - 1): N_CONTENT_PAGE * page]
                for content in list:
                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': Content.Categories(content.category).label.capitalize(),
                        'user': content.user.username,
                        'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                        'rev': content.rev
                    })
            elif filter == Content.Categories.MONSTERS:
                npages = int(1 + Content.objects.filter(category=Content.Categories.MONSTERS).count() / N_CONTENT_PAGE)

                list = Content.objects.filter(category=Content.Categories.MONSTERS)[
                       N_CONTENT_PAGE * (page - 1): N_CONTENT_PAGE * page]
                for content in list:
                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': Content.Categories(content.category).label.capitalize(),
                        'user': content.user.username,
                        'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                        'rev': content.rev
                    })
                pass
            elif filter == Content.Categories.SPELLS:
                npages = int(1 + Content.objects.filter(category=Content.Categories.SPELLS).count() / N_CONTENT_PAGE)

                list = Content.objects.filter(category=Content.Categories.SPELLS)[
                       N_CONTENT_PAGE * (page - 1): N_CONTENT_PAGE * page]
                for content in list:
                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': Content.Categories(content.category).label.capitalize(),
                        'user': content.user.username,
                        'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                        'rev': content.rev
                    })
                pass
            elif filter == FILTER_ALL:
                npages = int(1 + Content.objects.count() / N_CONTENT_PAGE)

                for content in Content.objects.all():

                    contentList.append({
                        'id': content.id,
                        'name': content.name,
                        'category': Content.Categories(content.category).label.capitalize(),
                        'user': content.user.username,
                        'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                        'rev': content.rev
                    })
            else:
                return render(request, self.template_name, context)

            if page > npages:
                page = npages
            if page < 1:
                page = 1

            context['page'] = page
            context['npages'] = npages

            if page < npages:
                context['nextPage'] = page + 1
            if page > 1:
                context['prevPage'] = page - 1

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
            print(detailForm.errors)
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
            shieldProficiency = False
            if 'shieldProficiency' in request.POST and request.POST['shieldProficiency'] == 'on':
                shieldProficiency = True

            detailContent = ClassContent(
                content = content,
                hitPointsLevel1 = request.POST['hitPointsLevel1'],
                hitPointsAboveLv1 = request.POST['hitPointsAboveLv1'],
                hitDiceType = request.POST['hitDiceType'],
                armorProficiency = request.POST['armorProficiency'],
                shieldProficiency = shieldProficiency,
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
            vComp = False
            if 'vComponent' in request.POST and request.POST['vComponent'] == 'on':
                vComp = True
            sComp = False
            if 'sComponent' in request.POST and request.POST['sComponent'] == 'on':
                sComp = True
            mComp = False
            if 'mComponent' in request.POST and request.POST['mComponent'] == 'on':
                mComp = True
            detailContent = SpellContent(
                content=content,
                level = request.POST['level'],
                castingTime = request.POST['castingTime'],
                range = request.POST['range'],
                vComponent = vComp,
                sComponent = sComp,
                mComponent = mComp,
                duration = request.POST['duration'],
                school = request.POST['school'],
            )

        detailContent.save()



        response = HttpResponseRedirect(redirect_to="./")
        response['Location'] += ('?detail=' + str(content.id))

        return response

# TODO ModifyContentView
class ModifyContentView(View):
    template_name = "grottadelbeholder/modify.html"

    def get(self, request):
        context = contextSetup(request)

        return render(request, self.template_name, context)
    def post(self, request):
        pass

# TODO UserContentView
class UserContentView(View):
    template_name = "grottadelbeholder/usercontent.html"

    def get(self, request):
        context = contextSetup(request)

        contentList = []
        list = Content.objects.filter(user_id=int(request.session[LOGGED_USER_ID]))

        for content in list:
            contentList.append({
                'id': content.id,
                'name': content.name,
                'category': Content.Categories(content.category).label.capitalize(),
                'user': content.user.username,
                'pub_date': str(content.pub_date.strftime("%d-%m-%Y")),
                'rev': content.rev
            })

        context['contentList'] = contentList

        return render(request, self.template_name, context)

# TODO DataTransferView
class DataTransferView(View):
    template_name = "grottadelbeholder/datatransfer.html"

    # Input di più contenuti da json
    def get(self, request):
        context = contextSetup(request)
        context['form'] = JsonFileUploadForm()

        return render(request, self.template_name, context)

    def post(self, request):
        if 'data' in request.FILES:
            print(request.content_type)


            if request.content_type == "application/json":
                file = ContentFile(request.FILES['data'])
                jsonData = file.read()

                print(jsonData)

def contextSetup(request):
    context = {}

    try:
        if userIsLogged(request):
            context[LOGGED_USER_NAME] = User.objects.get(id=request.session[LOGGED_USER_ID]).username


        adminType = userAdminType(request)

        if not adminType is None:
            context[ADMIN_TYPE_KEY] = adminType

    except:
        del request.session[LOGGED_USER_ID]
        del request.session[LOGGED_USER_NAME]
        del request.session[ADMIN_TYPE_KEY]

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