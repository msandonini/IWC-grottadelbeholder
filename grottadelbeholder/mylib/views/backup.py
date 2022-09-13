
import json
import mimetypes
from datetime import datetime

from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.views import View

from ProgettoIWC import settings
from grottadelbeholder.models import Content, RaceContent, ClassContent, MonsterContent, SpellContent, User, Admin
from grottadelbeholder.mylib.views.context import Context


BACKUP_FNAME = "backup.json"


# TODO DataTransferView
class DataTransferView(View):
    template_name = "grottadelbeholder/datatransfer.html"

    # Input di più contenuti da json
    def get(self, request):
        context = Context(request).getContext()

        print(request.GET)

        if "backup" in request.GET and request.GET["backup"] == "1":

            backupServer()

            fpath = settings.MEDIA_ROOT + "/" + BACKUP_FNAME

            with open(fpath, "r") as fout:
                mime_type, _ = mimetypes.guess_type(fpath)

                response = HttpResponse(fout, content_type=mime_type)
                response['Content-Disposition'] = "attachment; filename=%s" % BACKUP_FNAME

                return response

        return render(request, self.template_name, context)

    def post(self, request):
        file = request.FILES['data']
        fss = FileSystemStorage()
        fPc = fss.save(file.name, file)
        fUrl = fss.url(fPc)

        '''
        file = request.FILES['data'].file

        data = json.load(file)
        '''
        #todo post

        data = {}
        with open(settings.MEDIA_ROOT + "/" + file.name) as dataFile:
            data = json.load(dataFile)

            userSkip = []

            for user in data["Users"]:
                if not User.objects.filter(id=int(user["id"])).exists():
                    u = User(id=user["id"], username=user["username"], password=user["password"])
                    u.save()

            contentSkip = []

            for content in data["Content"]:
                cid = int(content["id"])
                uid = int(content["user_id"])
                if not User.objects.filter(id=uid).exists():
                    uid = User.objects.all()[0].id

                cat = Content.Categories(content["category"])

                date = datetime.strptime(content["pub_date"].split(".")[0], "%Y-%m-%d %H:%M:%S")
                rev = int(content["rev"])
                name = content["name"]
                descr = content["description"]

                if not Content.objects.filter(id=int(content["id"])).exists():
                    c = Content(id=cid, user=User.objects.get(id=uid), category=cat, pub_date=date, rev=rev, name=name, description=descr)
                    c.save()
                else:
                    contentSkip.append(cid)


            for race in data["Details"]["RaceContent"]:
                cid = race["id"]

                strInc = int(race["strScoreInc"])
                dexInc = int(race["dexScoreInc"])
                conInc = int(race["conScoreInc"])
                intInc = int(race["intScoreInc"])
                wisInc = int(race["wisScoreInc"])
                chaInc = int(race["chaScoreInc"])

                age = race["age"]
                align = race["alignment"]
                size = race["size"]
                speed = race["speed"]
                lang = race["languages"]
                sub = race["subraces"]

                r = RaceContent(content=Content.objects.get(id=cid), strScoreInc=strInc, dexScoreInc=dexInc, conScoreInc=conInc, intScoreInc=intInc, wisScoreInc=wisInc, chaScoreInc=chaInc, alignment=align, age=age, size=size, speed=speed, languages=lang, subraces=sub)
                r.save()
            for cl in data["Details"]["ClassContent"]:
                cid = cl["content_id"]

                hpl1 = cl["hitPointsLevel1"]
                hpa1 = cl["hitPointsAboveLv1"]
                hitd = ClassContent.DiceTypes(cl["hitDiceType"])
                aprof = ClassContent.ArmorProficiencies(cl["armorProficiency"])
                sprof = bool(cl["shieldProficiency"])
                wprof = cl["weaponProficiency"]
                tprof = cl["toolProficiency"]
                stprof = cl["savingThrows"]
                skprof = cl["skills"]
                tr = cl["traits"]
                arc = cl["archetypes"]

                c = ClassContent(content=Content.objects.get(id=cid), hitPointsLevel1=hpl1, hitPointsAboveLv1=hpa1, hitDiceType=hitd, armorProficiency=aprof, shieldProficiency=sprof, weaponProficiency=wprof, toolProficiency=tprof, savingThrows=stprof, skills=skprof, traits=tr, archetypes=arc)
                c.save()
            for mo in data["Details"]["MonsterContent"]:
                cid = mo["content_id"]

                ac = mo["armorClass"]
                hp = mo["hitPoints"]
                spd = mo["speed"]
                strS = mo["strScore"]
                dexS = mo["dexScore"]
                conS = mo["conScore"]
                intS = mo["intScore"]
                wisS = mo["wisScore"]
                chaS = mo["chaScore"]
                sk = mo["skills"]
                pp = mo["passivePerception"]
                cr = mo["challengeRate"]
                xp = mo["xp"]
                al = mo["alignment"]
                tr = mo["traits"]
                act = mo["actions"]

                m = MonsterContent(content=Content.objects.get(id=cid), armorClass=ac, hitPoints=hp, speed=spd, strScore=strS, dexScore=dexS, conScore=conS, intScore=intS, wisScore=wisS, chaScore=chaS, skills=sk, passivePerception=pp, challengeRate=cr, xp=xp, alignment=al, traits=tr, actions=act)
                m.save()
            for sp in data["Details"]["SpellContent"]:
                cid = sp["content_id"]

                lv = sp["level"]
                ct = sp["castingTime"]
                ra = sp["range"]
                vc = sp["vComponent"]
                sc = sp["sComponent"]
                mc = sp["mComponent"]
                du = sp["duration"]
                sch = sp["school"]

                s = SpellContent(content=Content.objects.get(id=cid), level=lv, castingTime=ct, range=ra, vComponent=vc, sComponent=sc, mComponent=mc, duration=du, school=sch)
                s.save()

            for skipped in contentSkip:
                print("Skipped restore of user id. " + str(skipped))
            for skipped in contentSkip:
                print("Skipped restore of content id. " + str(skipped))

        return HttpResponseRedirect(redirect_to="./")


def backupServer():
    dict = {
        "Users": list(User.objects.values()),
        "Content": list(Content.objects.values()),
        "Details": {
            "RaceContent": list(RaceContent.objects.values()),
            "ClassContent": list(ClassContent.objects.values()),
            "MonsterContent": list(MonsterContent.objects.values()),
            "SpellContent": list(SpellContent.objects.values())
        }
    }

    json_object = json.dumps(dict, indent=4, default=str)

    fss = FileSystemStorage()
    fss.save(BACKUP_FNAME, ContentFile(b""))

    with open(settings.MEDIA_ROOT + "/" + BACKUP_FNAME, "w") as file:
        file.write(json_object)

        file.close()
